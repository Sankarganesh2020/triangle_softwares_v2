from time import timezone
from django.db import models
import datetime
from uuid import uuid4
from django.template.defaultfilters import slugify
# from master.models import Style, Color, PartnerType, Size, Partner, Status, FabricType
# Create your models here.

class Job(models.Model):   
    job_no = models.CharField(primary_key=True, max_length=20, verbose_name='Job #')
    date = models.DateField(verbose_name='Order Date', default=datetime.date.today) 
    partner = models.ForeignKey('master.Partner', on_delete=models.CASCADE, verbose_name='Customer')    
    style = models.ForeignKey('master.Style', on_delete=models.CASCADE) 
    color = models.ForeignKey('master.Color', on_delete=models.CASCADE, blank=True, null=True)
    party_dc_no = models.CharField(max_length=20, verbose_name='Party DC #')   
    status = models.ForeignKey('master.Status', on_delete=models.CASCADE, verbose_name='Job Status',default="OPEN") 
    total_order_quantity = models.DecimalField(max_digits=30, decimal_places=0,default=0,null=True, blank=True)
    total_delivery_quantity = models.DecimalField(max_digits=30, decimal_places=0,default=0, null=True, blank=True)
    #Utility fields
    unique_id = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)    
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.unique_id is None:
            self.unique_id = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {} {}'.format(self.job_no, self.partner, self.unique_id))

        self.slug = slugify('{} {} {}'.format(self.job_no, self.partner, self.unique_id))


        super(Job, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.job_no

class Order(models.Model):
    job_no = models.ForeignKey('Job', on_delete=models.CASCADE)
    number = models.CharField(null=True, blank=True, max_length=16)
    # order_date = models.DateField('Order Date') 
    size = models.ForeignKey('master.Size', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=30, decimal_places=0,default=0)

    #Utility fields
    unique_id = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)     
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.unique_id is None:
            self.unique_id = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {} {}'.format(self.job_no, self.number, self.unique_id))

        self.slug = slugify('{} {} {}'.format(self.job_no, self.number, self.unique_id))


        super(Order, self).save(*args, **kwargs)



class FabricInward(models.Model):
    job_no = models.ForeignKey('Job', on_delete=models.CASCADE)
    number = models.CharField(null=True, blank=True, max_length=16)
    color = models.ForeignKey('master.Color', on_delete=models.CASCADE)
    party_dc_date = models.DateField('Party DC Date') 
    fabric_type = models.ForeignKey('master.FabricType', on_delete=models.CASCADE)
    no_of_rolls = models.DecimalField(max_digits=30, decimal_places=0,default=0, verbose_name='No of rolls')
    dc_weight = models.DecimalField(max_digits=30, decimal_places=3,default=0, verbose_name='DC Weight')
    received_weight = models.DecimalField(max_digits=30, decimal_places=3,default=0, verbose_name='Received Weight')
    
    
    #Utility fields
    unique_id = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True) 
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)    

    def save(self, *args, **kwargs):
        if self.unique_id is None:
            self.unique_id = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {} {}'.format(self.job_no, self.number, self.unique_id))

        self.slug = slugify('{} {} {}'.format(self.job_no, self.number, self.unique_id))


        super(FabricInward, self).save(*args, **kwargs)

class Delivery(models.Model): 
    job_no = models.ForeignKey('Job', on_delete=models.CASCADE)
    number = models.CharField(null=True, blank=True, max_length=16)
    date = models.DateField(verbose_name='Delivery Date', default=datetime.date.today)   
    size = models.ForeignKey('master.Size', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=30, decimal_places=0,default=0)
    piece_type = models.ForeignKey('master.PieceType', on_delete=models.CASCADE, blank=True, null=True)
    
    
    #Utility fields
    unique_id = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)     
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)  


    def save(self, *args, **kwargs):
        if self.unique_id is None:
            self.unique_id = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {} {}'.format(self.job_no, self.number, self.unique_id))

        self.slug = slugify('{} {} {}'.format(self.job_no, self.number, self.unique_id))


        super(Delivery, self).save(*args, **kwargs)
    
