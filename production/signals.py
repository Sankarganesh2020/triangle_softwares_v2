from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import *
from master.models import Status
from django.db.models import Sum

@receiver([post_save, post_delete], sender=Delivery)
def update_job_from_delivery(sender, instance, **kwargs):
    delivery_data = Delivery.objects.filter(job_no=instance.job_no)
    total_delivered_quantity = delivery_data.aggregate(Sum('quantity'))
    order_data = Order.objects.filter(job_no=instance.job_no)
    total_order_quantity = order_data.aggregate(Sum('quantity'))

    if total_order_quantity['quantity__sum'] == total_delivered_quantity['quantity__sum']:
        status =  Status.objects.get(pk='CLOSED')
    else:
        status = Status.objects.get(pk='OPEN')

    job_status = Status.objects.get(status=status)

    obj, created = Job.objects.update_or_create(
        job_no=instance.job_no.pk,
        defaults = {      
            'status' : job_status,
            'total_delivery_quantity': total_delivered_quantity['quantity__sum'],

        }
    )
                                
    print('Job updated!')    

@receiver([post_save, post_delete], sender=Order)
def update_job_from_order(sender, instance, **kwargs):

    order_data = Order.objects.filter(job_no=instance.job_no)
    total_order_quantity = order_data.aggregate(Sum('quantity'))


    obj, created = Job.objects.update_or_create(
        job_no=instance.job_no.pk,
        defaults = {      
            'total_order_quantity': total_order_quantity['quantity__sum'],

        }
    )
                                
    print('Job updated!')  

"""                             'color'=instance.job_no.color.pk,
                                'style'=instance.job_no.style.pk,
                                'rh'=instance.job_no.rh,
                                'size_s_quantity'=instance.job_no.size_s_quantity,
                                'size_m_quantity'=instance.job_no.size_m_quantity,
                                'size_l_quantity'=instance.job_no.size_l_quantity,
                                'size_xl_quantity'=instance.job_no.size_xl_quantity,
                                'size_2xl_quantity'=instance.job_no.size_2xl_quantity, """