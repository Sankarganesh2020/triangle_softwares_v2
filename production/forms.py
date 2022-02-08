from django import forms
from django.forms import widgets
from .models import *

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_no','date', 'partner', 'style', 'color', 'party_dc_no']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['size', 'quantity']

class DeliveryForm(forms.ModelForm):
    date = forms.DateField(
        label='Delivery Date', 
        widget=forms.widgets.DateInput(attrs={'type':'date'})
    )   

    class Meta:
        model = Delivery
        fields = ['date', 'size', 'quantity','piece_type']