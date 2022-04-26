from django import forms
from django.forms import widgets

from master.models import Size, Style, Color, Partner, PartnerType, FabricType
from .models import *


SIZE_CHOICES_LIST = Size.objects.all()
STYLE_CHOICES_LIST = Style.objects.all()
COLOR_CHOICES_LIST = Color.objects.all()
PARTNER_CHOICES_LIST = Partner.objects.all()
FABRIC_TYPE_CHOICES_LIST = FabricType.objects.all()
class JobForm(forms.ModelForm):
    job_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    party_dc_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    partner = forms.ModelChoiceField(queryset=PARTNER_CHOICES_LIST, label='Partner',
                                                  widget=forms.Select(attrs={'class': 'form-control'}))

    style = forms.ModelChoiceField(queryset=STYLE_CHOICES_LIST, to_field_name='style', label='Style',
                                                  widget=forms.Select(attrs={'class': 'form-control'}))   
    color = forms.ModelChoiceField(queryset=COLOR_CHOICES_LIST, to_field_name='color', label='Color',
                                                  widget=forms.Select(attrs={'class': 'form-control'}))                                                   
    class Meta:
        model = Job
        fields = ['job_no','partner', 'style', 'color', 'party_dc_no']

class OrderForm(forms.ModelForm):
    size = forms.ModelChoiceField(queryset=SIZE_CHOICES_LIST, to_field_name='size', label='Size',
                                              widget=forms.Select(attrs={'class': 'form-control'}))
    quantity = forms.DecimalField(decimal_places=0, widget=forms.NumberInput(attrs={'class': 'form-control'})) 
    class Meta:
        model = Order
        fields = ['size', 'quantity']

class FabricInwardForm(forms.ModelForm):
    color = forms.ModelChoiceField(queryset=COLOR_CHOICES_LIST, to_field_name='color', label='Color',
                                                  widget=forms.Select(attrs={'class': 'form-control'}))  
    fabric_type = forms.ModelChoiceField(queryset=FABRIC_TYPE_CHOICES_LIST,  label='Fabric Type',
                                                  widget=forms.Select(attrs={'class': 'form-control'}))           
    no_of_rolls = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))                                                  

    dc_weight = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))                                                  

    received_weight = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))                                                  

    class Meta:
        model = FabricInward
        fields = ['color', 'fabric_type','no_of_rolls','dc_weight','received_weight']

class DeliveryForm(forms.ModelForm):
    # date = forms.DateField(
    #     label='Delivery Date', 
    #     widget=forms.widgets.DateInput(attrs={'type':'date'})
    # )   
    size = forms.ModelChoiceField(queryset=SIZE_CHOICES_LIST, to_field_name='size', label='Size',  
                                                  widget=forms.Select(attrs={'class': 'form-control'}))
    quantity = forms.DecimalField(decimal_places=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))                                                  
    class Meta:
        model = Delivery
        fields = ['size', 'quantity']