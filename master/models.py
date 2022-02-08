from django.db import models

from django.db.models import Sum

# Create your models here.
class Style(models.Model):
    style = models.CharField(primary_key=True, max_length=20, verbose_name='Style')
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)      

    def __str__(self):
        return self.style

class Color(models.Model):
    color = models.CharField(primary_key=True, max_length=20, verbose_name='Color')
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)      

    def __str__(self):
        return self.color

class PartnerType(models.Model):
    partner_type = models.CharField(primary_key=True, max_length=20, verbose_name='Partner Type')
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.partner_type     

class Size(models.Model):
    size = models.CharField(max_length=5, verbose_name='Size')
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.size 

class Partner(models.Model):
    partner_name= models.CharField(max_length=60, verbose_name='Partner Name')
    partner_type = models.ForeignKey('PartnerType', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.partner_name  

class Status(models.Model):
    status = models.CharField(primary_key=True, max_length=20, verbose_name='Status')
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)     

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'

class FabricType(models.Model):
    fabric_type = models.CharField(max_length=60)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fabric_type

class PieceType(models.Model):
    piece_type = models.CharField(max_length=60)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.piece_type