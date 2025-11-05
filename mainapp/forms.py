from django import forms
from .models import LoadUnload, Party, Item


class PartyForm(forms.ModelForm):
    """Form for creating/editing Party"""
    
    class Meta:
        model = Party
        fields = ['name', 'address', 'phone']  # Exclude 'code' - it's auto-generated
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter party name',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Enter address',
                'rows': 3,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter phone number',
            }),
        }
        labels = {
            'name': 'Party Name',
            'address': 'Address',
            'phone': 'Phone Number',
        }


class ItemForm(forms.ModelForm):
    """Form for creating/editing Item"""
    
    class Meta:
        model = Item
        fields = ['name', 'description']  # Exclude 'code' - it's auto-generated
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter item name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Enter item description',
                'rows': 3,
            }),
        }
        labels = {
            'name': 'Item Name',
            'description': 'Description',
        }


class LoadUnloadForm(forms.ModelForm):
    """Form for creating Load/Unload transactions"""
    
    class Meta:
        model = LoadUnload
        fields = [
            'transaction_date',
            'transaction_type',
            'truck_no',
            'challan_no',
            'supplier',
            'customer',
            'item',
            'box_type',
            'box_qty',
            'qty_type',
            'quantity',
            'rate_per_qty',
            'total_amount',
            'remarks',
        ]
        widgets = {
            'transaction_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input',
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'truck_no': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter truck number',
            }),
            'challan_no': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter challan number',
            }),
            'supplier': forms.Select(attrs={
                'class': 'form-select',
            }),
            'customer': forms.Select(attrs={
                'class': 'form-select',
            }),
            'item': forms.Select(attrs={
                'class': 'form-select',
            }),
            'box_type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'box_qty': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter box quantity',
                'min': '1',
            }),
            'qty_type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter quantity',
                'step': '0.01',
                'min': '0',
            }),
            'rate_per_qty': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter rate per quantity',
                'step': '0.01',
                'min': '0',
            }),
            'total_amount': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Total amount (auto-calculated)',
                'step': '0.01',
                'readonly': 'readonly',
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Enter any remarks or notes',
                'rows': 3,
            }),
        }
        labels = {
            'transaction_date': 'Transaction Date',
            'transaction_type': 'Transaction Type',
            'truck_no': 'Truck Number',
            'challan_no': 'Challan Number',
            'supplier': 'Supplier/Receive From',
            'customer': 'Customer/Sent to',
            'item': 'Item',
            'box_type': 'Box Type',
            'box_qty': 'Box Quantity',
            'qty_type': 'Quantity Type',
            'quantity': 'Quantity',
            'rate_per_qty': 'Rate per Quantity',
            'total_amount': 'Total Amount',
            'remarks': 'Remarks',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set today's date as default
        if not self.instance.pk:
            from datetime import date
            self.fields['transaction_date'].initial = date.today()
        
        # Make certain fields required
        self.fields['transaction_date'].required = True
        self.fields['transaction_type'].required = True
        self.fields['truck_no'].required = True
        self.fields['challan_no'].required = True
        self.fields['item'].required = True
        
        # Supplier and Customer are conditionally required based on transaction type
        self.fields['supplier'].required = False
        self.fields['customer'].required = False

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        supplier = cleaned_data.get('supplier')
        customer = cleaned_data.get('customer')
        quantity = cleaned_data.get('quantity')
        rate_per_qty = cleaned_data.get('rate_per_qty')
        
        # Validate supplier/customer based on transaction type
        if transaction_type == 'Load':
            # For Load, customer is required
            if not customer:
                self.add_error('customer', 'Customer is required for Load transactions.')
        elif transaction_type == 'Unload':
            # For Unload, supplier is required
            if not supplier:
                self.add_error('supplier', 'Supplier is required for Unload transactions.')
        
        # Auto-calculate total amount
        if quantity and rate_per_qty:
            cleaned_data['total_amount'] = quantity * rate_per_qty
        
        return cleaned_data
