from dataclasses import fields
from django.contrib import admin

from import_export.admin import ImportExportMixin
from .models import Job, Order, FabricInward, Delivery
# Register your models here.

@admin.register(Job)
class JobAdmin(ImportExportMixin, admin.ModelAdmin):
    fields = ['job_no','date','partner', 'color','style','party_dc_no']
    list_display = ['job_no','date','partner', 'color', 'style','party_dc_no','status','total_order_quantity','total_delivery_quantity']
    list_filter = ['job_no','date','partner', 'color', 'style','party_dc_no','status']
    search_fields = ['job_no']
    exclude = ('status',)

@admin.register(Order)
class OrderAdmin(ImportExportMixin, admin.ModelAdmin):
    fields = ['job_no','number','size','quantity']
    list_display = ['job_no','number','size','quantity']
    list_filter = ['job_no','number','size']
    search_fields = ['job_no']   

@admin.register(FabricInward)
class FabricInwardAdmin(ImportExportMixin, admin.ModelAdmin):
    fields = ['job_no','number','color','party_dc_date','fabric_type','no_of_rolls','dc_weight','received_weight']
    list_display = ['job_no','number','color','party_dc_date','fabric_type','no_of_rolls','dc_weight','received_weight']
    list_filter = ['job_no','number','color','party_dc_date','fabric_type']
    search_fields = ['job_no']      

@admin.register(Delivery)
class DeliveryAdmin(ImportExportMixin, admin.ModelAdmin):
    fields = ['job_no','number','date','size','quantity','piece_type']
    list_display = ['job_no','number','date','size','quantity','piece_type']
    list_filter = ['job_no','number','date','size','piece_type']
    search_fields = ['job_no']       