from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms

# Optional: custom form for more control
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # or your dashboard

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # or your target page
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

from django.shortcuts import render
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Policy, Payment, Claim, Customer, User, InsuranceProduct
from django.db.models.functions import TruncMonth

def dashboard_view(request):
    # Calculate time ranges
    today = timezone.now().date()
    last_month = today - timedelta(days=30)
    last_year = today - timedelta(days=365)
    
    # Policy statistics
    total_policies = Policy.objects.count()
    active_policies = Policy.objects.filter(status='active').count()
    new_policies_month = Policy.objects.filter(created_at__gte=last_month).count()
    
    # Payment statistics
    monthly_premiums = Payment.objects.filter(
        payment_type='premium',
        payment_date__month=today.month,
        payment_date__year=today.year
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    claims_paid = Payment.objects.filter(
        payment_type='claim',
        payment_date__year=today.year
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Claim statistics
    total_claims = Claim.objects.count()
    claims_this_month = Claim.objects.filter(reported_date__month=today.month).count()
    claims_pending = Claim.objects.filter(status='reported').count()
    
    # Customer statistics
    total_customers = Customer.objects.count()
    new_customers_month = Customer.objects.filter(created_at__gte=last_month).count()
    
    # Latest records for tables
    latest_payments = Payment.objects.select_related('customer', 'policy').order_by('-payment_date')[:5]
    latest_claims = Claim.objects.select_related('policy').order_by('-reported_date')[:3]
    
     # Policy growth data for chart (last 12 months)
    policy_growth = Policy.objects.filter(
        created_at__gte=last_year
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    # Customer growth data for chart
    customer_growth = Customer.objects.filter(
        created_at__gte=last_year
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    # Product distribution data
    product_distribution = InsuranceProduct.objects.annotate(
        policy_count=Count('policy')
    ).values('name', 'policy_count')
    
    context = {
        'total_policies': total_policies,
        'active_policies': active_policies,
        'new_policies_month': new_policies_month,
        'monthly_premiums': monthly_premiums,
        'claims_paid': claims_paid,
        'total_claims': total_claims,
        'claims_this_month': claims_this_month,
        'claims_pending': claims_pending,
        'total_customers': total_customers,
        'new_customers_month': new_customers_month,
        'latest_payments': latest_payments,
        'latest_claims': latest_claims,
        'policy_growth': list(policy_growth),
        'customer_growth': list(customer_growth),
        'product_distribution': list(product_distribution),
    }
    
    return render(request, 'dashboard/dashboard.html', context)