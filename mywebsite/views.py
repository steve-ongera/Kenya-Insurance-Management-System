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
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from .models import Customer, Policy, Claim, Payment, Commission, InsuranceProduct

@login_required
def dashboard_view(request):
    context = {
        'total_customers': Customer.objects.count(),
        'total_policies': Policy.objects.count(),
        'active_policies': Policy.objects.filter(status='active').count(),
        'expired_policies': Policy.objects.filter(status='expired').count(),

        'total_claims': Claim.objects.count(),
        'approved_claims': Claim.objects.filter(status='approved').count(),
        'settled_claims': Claim.objects.filter(status='settled').count(),
        'pending_claims': Claim.objects.filter(status__in=['reported', 'investigating', 'processing']).count(),

        'total_premiums': Policy.objects.aggregate(total=Sum('premium_amount'))['total'] or 0,
        'total_claims_paid': Claim.objects.aggregate(total=Sum('paid_amount'))['total'] or 0,

        'total_payments': Payment.objects.filter(payment_type='premium').aggregate(total=Sum('amount'))['total'] or 0,
        'claim_payouts': Payment.objects.filter(payment_type='claim').aggregate(total=Sum('amount'))['total'] or 0,

        'total_commissions': Commission.objects.aggregate(total=Sum('commission_amount'))['total'] or 0,
    }

    return render(request, 'dashboard/dashboard.html', context)
