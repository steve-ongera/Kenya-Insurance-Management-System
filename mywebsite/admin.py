from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Sum, Count
from django.contrib.admin import SimpleListFilter
import datetime

from .models import (
    User, Branch, Customer, InsuranceProduct, Policy, PolicyBenefit, 
    PolicyRider, Quotation, Claim, ClaimDocument, Payment, Commission,
    RiskAssessment, ReinsuranceContract, AuditLog, SystemConfiguration
)


# Custom Filters
class DateRangeFilter(SimpleListFilter):
    title = 'Date Range'
    parameter_name = 'date_range'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Today'),
            ('this_week', 'This Week'),
            ('this_month', 'This Month'),
            ('this_year', 'This Year'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            return queryset.filter(created_at__date=datetime.date.today())
        elif self.value() == 'this_week':
            return queryset.filter(created_at__week=datetime.date.today().isocalendar()[1])
        elif self.value() == 'this_month':
            return queryset.filter(created_at__month=datetime.date.today().month)
        elif self.value() == 'this_year':
            return queryset.filter(created_at__year=datetime.date.today().year)


class PolicyStatusFilter(SimpleListFilter):
    title = 'Policy Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('active', 'Active'),
            ('expired', 'Expired'),
            ('cancelled', 'Cancelled'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())


# Inline Admin Classes
class PolicyBenefitInline(admin.TabularInline):
    model = PolicyBenefit
    extra = 1
    fields = ['benefit_name', 'coverage_limit', 'description']


class PolicyRiderInline(admin.TabularInline):
    model = PolicyRider
    extra = 0
    fields = ['rider_name', 'premium_amount', 'coverage_amount', 'description']


class ClaimDocumentInline(admin.TabularInline):
    model = ClaimDocument
    extra = 0
    fields = ['document_type', 'file', 'description', 'uploaded_by']
    readonly_fields = ['uploaded_by']


class CommissionInline(admin.TabularInline):
    model = Commission
    extra = 0
    fields = ['agent', 'commission_rate', 'commission_amount', 'status']
    readonly_fields = ['commission_amount']


# Main Admin Classes
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'branch', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_active', 'is_staff', 'branch']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'national_id', 'employee_id']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Insurance System Info', {
            'fields': ('user_type', 'phone_number', 'national_id', 'employee_id', 'branch', 'is_verified')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Insurance System Info', {
            'fields': ('user_type', 'phone_number', 'national_id', 'employee_id', 'branch')
        }),
    )


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'town', 'county', 'manager', 'phone_number', 'is_active']
    list_filter = ['county', 'is_active']
    search_fields = ['name', 'code', 'town', 'county']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'manager')
        }),
        ('Location', {
            'fields': ('address', 'town', 'county')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_number', 'get_full_name', 'customer_type', 'phone_number', 'email', 'agent', 'branch', 'is_active']
    list_filter = ['customer_type', 'county', 'branch', 'is_active', DateRangeFilter]
    search_fields = ['customer_number', 'first_name', 'last_name', 'company_name', 'phone_number', 'email', 'national_id', 'kra_pin']
    ordering = ['-created_at']
    
    def get_full_name(self, obj):
        if obj.customer_type == 'individual':
            return f"{obj.first_name} {obj.last_name}"
        return obj.company_name
    get_full_name.short_description = 'Name'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('customer_number', 'customer_type', 'branch', 'agent')
        }),
        ('Individual Customer', {
            'fields': ('first_name', 'middle_name', 'last_name', 'gender', 'date_of_birth', 'national_id', 'passport_number'),
            'classes': ('collapse',)
        }),
        ('Corporate Customer', {
            'fields': ('company_name', 'registration_number', 'kra_pin', 'business_type'),
            'classes': ('collapse',)
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email', 'postal_address', 'physical_address', 'town', 'county')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('branch', 'agent')


@admin.register(InsuranceProduct)
class InsuranceProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'category', 'minimum_premium', 'commission_rate', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering = ['category', 'name']
    
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'code', 'category', 'description')
        }),
        ('Financial Details', {
            'fields': ('minimum_premium', 'maximum_coverage', 'commission_rate')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ['policy_number', 'customer', 'product', 'status', 'premium_amount', 'start_date', 'end_date', 'agent']
    list_filter = ['status', 'product__category', 'payment_frequency', 'branch', PolicyStatusFilter, DateRangeFilter]
    search_fields = ['policy_number', 'customer__first_name', 'customer__last_name', 'customer__company_name']
    ordering = ['-created_at']
    date_hierarchy = 'start_date'
    inlines = [PolicyBenefitInline, PolicyRiderInline, CommissionInline]
    
    fieldsets = (
        ('Policy Information', {
            'fields': ('policy_number', 'customer', 'product', 'status')
        }),
        ('Business Details', {
            'fields': ('branch', 'agent', 'underwriter')
        }),
        ('Coverage Details', {
            'fields': ('start_date', 'end_date', 'premium_amount', 'sum_insured', 'deductible')
        }),
        ('Payment Terms', {
            'fields': ('payment_frequency',)
        }),
        ('Additional Information', {
            'fields': ('policy_conditions', 'special_terms'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer', 'product', 'agent', 'branch')
    
    actions = ['mark_as_active', 'mark_as_expired']
    
    def mark_as_active(self, request, queryset):
        queryset.update(status='active')
    mark_as_active.short_description = "Mark selected policies as active"
    
    def mark_as_expired(self, request, queryset):
        queryset.update(status='expired')
    mark_as_expired.short_description = "Mark selected policies as expired"


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ['quotation_number', 'customer', 'product', 'status', 'premium_amount', 'valid_until', 'agent']
    list_filter = ['status', 'product__category', DateRangeFilter]
    search_fields = ['quotation_number', 'customer__first_name', 'customer__last_name', 'customer__company_name']
    ordering = ['-created_at']
    date_hierarchy = 'valid_until'
    
    fieldsets = (
        ('Quotation Information', {
            'fields': ('quotation_number', 'customer', 'product', 'agent', 'status')
        }),
        ('Quote Details', {
            'fields': ('premium_amount', 'sum_insured', 'valid_until')
        }),
        ('Terms & Conditions', {
            'fields': ('terms_conditions',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ['claim_number', 'policy', 'claim_type', 'status', 'claimed_amount', 'approved_amount', 'incident_date', 'assigned_to']
    list_filter = ['status', 'claim_type', 'policy__product__category', DateRangeFilter]
    search_fields = ['claim_number', 'policy__policy_number', 'policy__customer__first_name', 'policy__customer__last_name']
    ordering = ['-created_at']
    date_hierarchy = 'incident_date'
    inlines = [ClaimDocumentInline]
    
    fieldsets = (
        ('Claim Information', {
            'fields': ('claim_number', 'policy', 'claim_type', 'status', 'assigned_to')
        }),
        ('Incident Details', {
            'fields': ('incident_date', 'incident_description', 'incident_location', 'police_report_number')
        }),
        ('Financial Information', {
            'fields': ('claimed_amount', 'assessed_amount', 'approved_amount', 'paid_amount')
        }),
        ('Processing Details', {
            'fields': ('surveyor', 'surveyor_report', 'decline_reason'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('policy', 'policy__customer', 'assigned_to')
    
    actions = ['approve_claims', 'decline_claims']
    
    def approve_claims(self, request, queryset):
        queryset.update(status='approved')
    approve_claims.short_description = "Approve selected claims"
    
    def decline_claims(self, request, queryset):
        queryset.update(status='declined')
    decline_claims.short_description = "Decline selected claims"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_reference', 'payment_type', 'customer', 'amount', 'payment_method', 'status', 'payment_date']
    list_filter = ['payment_type', 'payment_method', 'status', DateRangeFilter]
    search_fields = ['payment_reference', 'transaction_id', 'mpesa_receipt', 'customer__first_name', 'customer__last_name']
    ordering = ['-payment_date']
    date_hierarchy = 'payment_date'
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('payment_reference', 'payment_type', 'customer', 'policy', 'claim')
        }),
        ('Financial Details', {
            'fields': ('amount', 'transaction_fee', 'net_amount', 'payment_method', 'status')
        }),
        ('Transaction Details', {
            'fields': ('transaction_id', 'mpesa_receipt', 'cheque_number', 'bank_reference')
        }),
        ('Dates', {
            'fields': ('payment_date', 'due_date')
        }),
        ('Processing', {
            'fields': ('processed_by',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer', 'policy', 'claim', 'processed_by')


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ['agent', 'policy', 'commission_rate', 'commission_amount', 'status', 'payment_date']
    list_filter = ['status', 'agent__branch', DateRangeFilter]
    search_fields = ['agent__username', 'policy__policy_number']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Commission Information', {
            'fields': ('agent', 'policy', 'payment')
        }),
        ('Financial Details', {
            'fields': ('commission_rate', 'commission_amount', 'status')
        }),
        ('Processing', {
            'fields': ('payment_date', 'approved_by')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('agent', 'policy', 'approved_by')


@admin.register(RiskAssessment)
class RiskAssessmentAdmin(admin.ModelAdmin):
    list_display = ['policy', 'risk_category', 'risk_score', 'vehicle_make', 'vehicle_model', 'driver_age']
    list_filter = ['risk_category', 'medical_report_required', 'property_inspection_required']
    search_fields = ['policy__policy_number', 'vehicle_make', 'vehicle_model', 'registration_number']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Policy Information', {
            'fields': ('policy',)
        }),
        ('Vehicle Information', {
            'fields': ('vehicle_make', 'vehicle_model', 'vehicle_year', 'vehicle_value', 'registration_number', 'engine_number', 'chassis_number')
        }),
        ('Driver Information', {
            'fields': ('driver_age', 'driving_experience', 'previous_claims')
        }),
        ('Risk Assessment', {
            'fields': ('risk_score', 'risk_category')
        }),
        ('Additional Requirements', {
            'fields': ('medical_report_required', 'property_inspection_required', 'additional_requirements')
        }),
    )


@admin.register(ReinsuranceContract)
class ReinsuranceContractAdmin(admin.ModelAdmin):
    list_display = ['contract_number', 'reinsurer_name', 'contract_type', 'product', 'effective_date', 'expiry_date']
    list_filter = ['contract_type', 'product__category']
    search_fields = ['contract_number', 'reinsurer_name']
    ordering = ['-effective_date']
    
    fieldsets = (
        ('Contract Information', {
            'fields': ('contract_number', 'reinsurer_name', 'contract_type', 'product')
        }),
        ('Terms', {
            'fields': ('effective_date', 'expiry_date', 'retention_limit', 'reinsurance_rate')
        }),
        ('Additional Terms', {
            'fields': ('terms_conditions',),
            'classes': ('collapse',)
        }),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action_type', 'model_name', 'object_id', 'created_at', 'ip_address']
    list_filter = ['action_type', 'model_name', DateRangeFilter]
    search_fields = ['user__username', 'model_name', 'object_id', 'description']
    ordering = ['-created_at']
    readonly_fields = ['user', 'action_type', 'model_name', 'object_id', 'description', 'ip_address', 'user_agent', 'created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'data_type', 'is_active']
    list_filter = ['data_type', 'is_active']
    search_fields = ['key', 'description']
    ordering = ['key']
    
    fieldsets = (
        ('Configuration', {
            'fields': ('key', 'value', 'data_type')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


# Register remaining models with basic admin
@admin.register(PolicyBenefit)
class PolicyBenefitAdmin(admin.ModelAdmin):
    list_display = ['policy', 'benefit_name', 'coverage_limit']
    list_filter = ['policy__product__category']
    search_fields = ['policy__policy_number', 'benefit_name']


@admin.register(PolicyRider)
class PolicyRiderAdmin(admin.ModelAdmin):
    list_display = ['policy', 'rider_name', 'premium_amount', 'coverage_amount']
    list_filter = ['policy__product__category']
    search_fields = ['policy__policy_number', 'rider_name']


@admin.register(ClaimDocument)
class ClaimDocumentAdmin(admin.ModelAdmin):
    list_display = ['claim', 'document_type', 'uploaded_by', 'created_at']
    list_filter = ['document_type', DateRangeFilter]
    search_fields = ['claim__claim_number', 'description']


# Customize Admin Site
admin.site.site_header = "Kenya Insurance Management System"
admin.site.site_title = "Insurance Admin"
admin.site.index_title = "Welcome to Insurance Management System"

# Add custom CSS for better styling
class AdminConfig:
    def __init__(self):
        pass
    
    @staticmethod
    def get_app_list(self, request):
        """
        Custom ordering of admin apps
        """
        app_dict = self._build_app_dict(request)
        
        # Custom app ordering
        app_order = [
            'Dashboard',
            'Customers',
            'Policies', 
            'Claims',
            'Payments',
            'Products',
            'Users',
            'Reports',
            'System'
        ]
        
        return app_dict