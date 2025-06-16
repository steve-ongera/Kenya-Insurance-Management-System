from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from decimal import Decimal
import uuid
from datetime import date, datetime


class BaseModel(models.Model):
    """Base model with common fields"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True


class User(AbstractUser):
    """Extended user model for the insurance system"""
    USER_TYPES = [
        ('admin', 'Administrator'),
        ('agent', 'Insurance Agent'),
        ('underwriter', 'Underwriter'),
        ('claims_officer', 'Claims Officer'),
        ('customer_service', 'Customer Service'),
        ('finance', 'Finance Officer'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='agent')
    phone_number = models.CharField(max_length=15, unique=True)
    national_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Branch(BaseModel):
    """Insurance company branches"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    address = models.TextField()
    county = models.CharField(max_length=50)
    town = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='managed_branches')
    
    def __str__(self):
        return f"{self.name} - {self.town}"


class Customer(BaseModel):
    """Customer/Policyholder model"""
    CUSTOMER_TYPES = [
        ('individual', 'Individual'),
        ('corporate', 'Corporate'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    customer_number = models.CharField(max_length=20, unique=True)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES)
    
    # Individual customer fields
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    middle_name = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    national_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    passport_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    # Corporate customer fields
    company_name = models.CharField(max_length=200, blank=True)
    registration_number = models.CharField(max_length=50, blank=True)
    kra_pin = models.CharField(max_length=20, blank=True)
    business_type = models.CharField(max_length=100, blank=True)
    
    # Common contact fields
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    postal_address = models.CharField(max_length=200)
    physical_address = models.TextField()
    county = models.CharField(max_length=50)
    town = models.CharField(max_length=50)
    
    # Business fields
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='customers')
    
    def __str__(self):
        if self.customer_type == 'individual':
            return f"{self.first_name} {self.last_name}"
        return self.company_name


class InsuranceProduct(BaseModel):
    """Insurance products offered by the company"""
    PRODUCT_CATEGORIES = [
        ('motor', 'Motor Insurance'),
        ('health', 'Health Insurance'),
        ('life', 'Life Insurance'),
        ('property', 'Property Insurance'),
        ('marine', 'Marine Insurance'),
        ('aviation', 'Aviation Insurance'),
        ('liability', 'Liability Insurance'),
        ('travel', 'Travel Insurance'),
        ('agriculture', 'Agriculture Insurance'),
    ]
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=20, choices=PRODUCT_CATEGORIES)
    description = models.TextField()
    minimum_premium = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    maximum_coverage = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Percentage
    
    def __str__(self):
        return f"{self.name} ({self.category})"


class Policy(BaseModel):
    """Insurance policies"""
    POLICY_STATUS = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('suspended', 'Suspended'),
        ('lapsed', 'Lapsed'),
    ]
    
    policy_number = models.CharField(max_length=30, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='policies')
    product = models.ForeignKey(InsuranceProduct, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='policies')
    underwriter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='underwritten_policies')
    
    # Policy details
    status = models.CharField(max_length=20, choices=POLICY_STATUS, default='draft')
    start_date = models.DateField()
    end_date = models.DateField()
    premium_amount = models.DecimalField(max_digits=15, decimal_places=2)
    sum_insured = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Payment terms
    payment_frequency = models.CharField(max_length=20, choices=[
        ('annual', 'Annual'),
        ('semi_annual', 'Semi-Annual'),
        ('quarterly', 'Quarterly'),
        ('monthly', 'Monthly'),
    ], default='annual')
    
    # Additional fields
    policy_conditions = models.TextField(blank=True)
    special_terms = models.TextField(blank=True)
    deductible = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.policy_number} - {self.customer}"


class PolicyBenefit(BaseModel):
    """Benefits covered under each policy"""
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='benefits')
    benefit_name = models.CharField(max_length=100)
    coverage_limit = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.policy.policy_number} - {self.benefit_name}"


class PolicyRider(BaseModel):
    """Additional riders/add-ons to policies"""
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='riders')
    rider_name = models.CharField(max_length=100)
    premium_amount = models.DecimalField(max_digits=15, decimal_places=2)
    coverage_amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.policy.policy_number} - {self.rider_name}"


class Quotation(BaseModel):
    """Insurance quotations"""
    QUOTATION_STATUS = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('expired', 'Expired'),
        ('converted', 'Converted to Policy'),
    ]
    
    quotation_number = models.CharField(max_length=30, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='quotations')
    product = models.ForeignKey(InsuranceProduct, on_delete=models.CASCADE)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='quotations')
    
    status = models.CharField(max_length=20, choices=QUOTATION_STATUS, default='draft')
    valid_until = models.DateField()
    premium_amount = models.DecimalField(max_digits=15, decimal_places=2)
    sum_insured = models.DecimalField(max_digits=15, decimal_places=2)
    terms_conditions = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.quotation_number} - {self.customer}"


class Claim(BaseModel):
    """Insurance claims"""
    CLAIM_STATUS = [
        ('reported', 'Reported'),
        ('investigating', 'Under Investigation'),
        ('processing', 'Processing'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('settled', 'Settled'),
        ('closed', 'Closed'),
    ]
    
    CLAIM_TYPES = [
        ('total_loss', 'Total Loss'),
        ('partial_loss', 'Partial Loss'),
        ('theft', 'Theft'),
        ('accident', 'Accident'),
        ('medical', 'Medical'),
        ('death', 'Death'),
        ('disability', 'Disability'),
        ('property_damage', 'Property Damage'),
        ('other', 'Other'),
    ]
    
    claim_number = models.CharField(max_length=30, unique=True)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='claims')
    claim_type = models.CharField(max_length=20, choices=CLAIM_TYPES)
    status = models.CharField(max_length=20, choices=CLAIM_STATUS, default='reported')
    
    # Claim details
    incident_date = models.DateField()
    reported_date = models.DateField(auto_now_add=True)
    incident_description = models.TextField()
    incident_location = models.CharField(max_length=200)
    police_report_number = models.CharField(max_length=50, blank=True)
    
    # Financial details
    claimed_amount = models.DecimalField(max_digits=15, decimal_places=2)
    assessed_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    approved_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Processing
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_claims')
    surveyor = models.CharField(max_length=100, blank=True)
    surveyor_report = models.TextField(blank=True)
    decline_reason = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.claim_number} - {self.policy.policy_number}"


class ClaimDocument(BaseModel):
    """Documents related to claims"""
    DOCUMENT_TYPES = [
        ('police_report', 'Police Report'),
        ('medical_report', 'Medical Report'),
        ('repair_estimate', 'Repair Estimate'),
        ('photos', 'Photos'),
        ('receipts', 'Receipts'),
        ('death_certificate', 'Death Certificate'),
        ('other', 'Other'),
    ]
    
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='claim_documents/')
    description = models.CharField(max_length=200, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.claim.claim_number} - {self.document_type}"


class Payment(BaseModel):
    """Premium and claim payments"""
    PAYMENT_TYPES = [
        ('premium', 'Premium Payment'),
        ('claim', 'Claim Payment'),
        ('refund', 'Refund'),
        ('commission', 'Commission'),
    ]
    
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
        ('card', 'Credit/Debit Card'),
        ('online', 'Online Payment'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    payment_reference = models.CharField(max_length=50, unique=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    
    # References
    policy = models.ForeignKey(Policy, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    claim = models.ForeignKey(Claim, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    
    # Payment details
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=15, decimal_places=2)
    
    # External references
    transaction_id = models.CharField(max_length=100, blank=True)
    mpesa_receipt = models.CharField(max_length=50, blank=True)
    cheque_number = models.CharField(max_length=50, blank=True)
    bank_reference = models.CharField(max_length=100, blank=True)
    
    # Dates
    payment_date = models.DateTimeField()
    due_date = models.DateField(null=True, blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.payment_reference} - {self.amount}"


class Commission(BaseModel):
    """Agent commissions"""
    COMMISSION_STATUS = [
        ('calculated', 'Calculated'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('disputed', 'Disputed'),
    ]
    
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commissions')
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='commissions')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=COMMISSION_STATUS, default='calculated')
    
    payment_date = models.DateField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_commissions')
    
    def __str__(self):
        return f"{self.agent.username} - {self.commission_amount}"


class RiskAssessment(BaseModel):
    """Risk assessment for policies (especially motor)"""
    policy = models.OneToOneField(Policy, on_delete=models.CASCADE, related_name='risk_assessment')
    
    # Motor specific fields
    vehicle_make = models.CharField(max_length=50, blank=True)
    vehicle_model = models.CharField(max_length=50, blank=True)
    vehicle_year = models.IntegerField(null=True, blank=True)
    vehicle_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    registration_number = models.CharField(max_length=20, blank=True)
    engine_number = models.CharField(max_length=50, blank=True)
    chassis_number = models.CharField(max_length=50, blank=True)
    
    # Driver information
    driver_age = models.IntegerField(null=True, blank=True)
    driving_experience = models.IntegerField(null=True, blank=True, help_text="Years of driving experience")
    previous_claims = models.IntegerField(default=0)
    
    # Risk factors
    risk_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    risk_category = models.CharField(max_length=20, choices=[
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
    ], default='medium')
    
    # Additional assessments
    medical_report_required = models.BooleanField(default=False)
    property_inspection_required = models.BooleanField(default=False)
    additional_requirements = models.TextField(blank=True)
    
    def __str__(self):
        return f"Risk Assessment - {self.policy.policy_number}"


class ReinsuranceContract(BaseModel):
    """Reinsurance contracts"""
    CONTRACT_TYPES = [
        ('quota_share', 'Quota Share'),
        ('surplus', 'Surplus'),
        ('excess_of_loss', 'Excess of Loss'),
        ('stop_loss', 'Stop Loss'),
    ]
    
    contract_number = models.CharField(max_length=30, unique=True)
    reinsurer_name = models.CharField(max_length=100)
    contract_type = models.CharField(max_length=20, choices=CONTRACT_TYPES)
    product = models.ForeignKey(InsuranceProduct, on_delete=models.CASCADE)
    
    effective_date = models.DateField()
    expiry_date = models.DateField()
    retention_limit = models.DecimalField(max_digits=15, decimal_places=2)
    reinsurance_rate = models.DecimalField(max_digits=5, decimal_places=2)
    
    terms_conditions = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.contract_number} - {self.reinsurer_name}"


class AuditLog(BaseModel):
    """Audit trail for important actions"""
    ACTION_TYPES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('approve', 'Approve'),
        ('decline', 'Decline'),
        ('payment', 'Payment'),
        ('login', 'Login'),
        ('logout', 'Logout'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    model_name = models.CharField(max_length=50)
    object_id = models.CharField(max_length=50)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user} - {self.action_type} - {self.model_name}"


class SystemConfiguration(BaseModel):
    """System configuration settings"""
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    data_type = models.CharField(max_length=20, choices=[
        ('string', 'String'),
        ('integer', 'Integer'),
        ('decimal', 'Decimal'),
        ('boolean', 'Boolean'),
        ('json', 'JSON'),
    ], default='string')
    
    def __str__(self):
        return f"{self.key}: {self.value}"