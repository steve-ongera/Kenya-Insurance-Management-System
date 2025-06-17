from django import forms
from .models import Customer


class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'customer_type',
            'first_name', 'middle_name', 'last_name',
            'gender', 'date_of_birth', 'national_id',
            'company_name', 'registration_number', 'kra_pin', 'business_type',
            'phone_number', 'email',
            'physical_address', 'postal_address',
            'town', 'county',
            'branch', 'agent'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'physical_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):  # Avoid adding form-control to checkboxes
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f'{existing_classes} form-control'.strip()
