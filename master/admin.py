from django.contrib import admin

from import_export.admin import ImportExportMixin
from .models import Style, Color, PartnerType, Size, Partner, Status, FabricType, PieceType

# Register your models here.
admin.site.site_header = "Triangle Clothing"
admin.site.site_title = "Triangle Clothing"
admin.site.index_title = "Manage Triangle Clothing"

@admin.register(Style)
class StyleAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['style','created_on','modified_on']
    search_fields = ['style']

@admin.register(Color)
class ColorAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['color','created_on','modified_on']
    search_fields = ['color']    

@admin.register(PartnerType)
class PartnerTypeAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['partner_type','created_on','modified_on']
    search_fields = ['partner_type']

@admin.register(Size)
class SizeAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['size','created_on','modified_on']
    search_fields = ['size']

@admin.register(Partner)
class PartnerAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['partner_name','partner_type','created_on','modified_on']
    search_fields = ['partner_name']  

@admin.register(Status)
class StatusAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['status','created_on','modified_on']
    search_fields = ['status'] 

@admin.register(FabricType)
class FabricTypeAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['fabric_type','created_on','modified_on']
    search_fields = ['fabric_type']     

@admin.register(PieceType)
class PieceTypeAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['piece_type','created_on','modified_on']
    search_fields = ['piece_type']      