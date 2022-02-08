from dataclasses import fields
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.forms.formsets import formset_factory
from django.forms import inlineformset_factory, modelformset_factory
from django.db.models import Sum
import pandas as pd
import json

from .models import *
from .forms import *
from .filters import *

from .functions import *
# Create your views here.

# @login_required(login_url="/authentication/login/")
# def list_jobs(request):
#     context = {}
#     jobs = Job.objects.all()
#     context['jobs'] = jobs

#     return render(request, 'production/jobs_list.html', context)
    # return render(request, 'home/transactions.html', context)

@login_required(login_url="/authentication/login/")
def list_jobs(request):
    # OrderFormSet = inlineformset_factory(Job, Order, fields=('id','size', 'quantity',), can_delete=False)
    OrderFormSet = formset_factory(OrderForm, extra=6, max_num=6, validate_min=True)
    context = {}
    msg = None
    jobs = Job.objects.all()
    
    # order_summary= order_data.values('job_no','job_no__date','job_no__status','job_no__color','job_no__style').annotate(total_qty=Sum('quantity'))
    MyJobFilter = JobFilter(request.GET, queryset=jobs)

    jobs = MyJobFilter.qs

    context['jobs'] = jobs

    context['MyJobFilter'] = MyJobFilter
    context['title'] = "Add Job"

    if request.method == 'GET':
        form = JobForm()
        formset = OrderFormSet()

        context['form'] = form
        context['formset'] = formset
        return render(request, 'production/jobs_list.html', context)

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        formset = OrderFormSet(request.POST, request.FILES)
        order_number = increment_order_number()

        if all([form.is_valid(), formset.is_valid()]) :
            job = form.save()
            for inline_form in formset:
                if inline_form.cleaned_data:
                    order = inline_form.save(commit=False)
                    order.job_no = job 
                    order.number = order_number                   
                    order.save()
                    messages.success(request, 'New Job has been Added')
                    msg = 'New Job has been Added'
            return redirect('production:jobs-list')
        else:
            messages.error(request, 'Problem processing your request')
            msg = 'Problem processing your request'
            return redirect('production:jobs-list')

    context['msg'] = msg
    return render(request, 'production/jobs_list.html', context)

@login_required(login_url="/authentication/login/")
def edit_jobs(request, slug):
    OrderFormSet = inlineformset_factory(Job, Order, fields=('size', 'quantity',), can_delete=False, extra=6)
    # OrderFormSet = formset_factory(OrderForm, extra=6, max_num=6, validate_min=True)
    context = {}
    msg = None
    job = Job.objects.get(slug=slug)
    context['title'] = "Edit Job"

    if request.method == 'GET':
        form = JobForm(instance=job)
        formset = OrderFormSet(instance=job)

        context['form'] = form
        context['formset'] = formset
        return render(request, 'production/jobs_edit.html', context)

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=job)
        formset = OrderFormSet(request.POST, request.FILES, instance=job)

        if formset.is_valid():
            if form.is_valid():
                job = form.save()
            for inline_form in formset:
                if inline_form.cleaned_data:
                    order = inline_form.save(commit=False)
                    order.job_no = job  
                    # order.number =  increment_order_number()                  
                    order.save()
                    messages.success(request, 'New Job has been Added')
                    msg = 'New Job has been Added'
            return redirect('production:jobs-list')
        else:
            messages.error(request, 'Problem processing your request')
            msg = 'Problem processing your request'
            return redirect('production:jobs-list')

    context['msg'] = msg
    return render(request, 'production/jobs_edit.html', context)    



@login_required(login_url="/authentication/login/")
def details_job(request, slug):
    job = Job.objects.get(slug=slug)
    orders_qs = Order.objects.filter(job_no=job)
    orders = orders_qs.annotate(total_quantity=Sum('quantity')).values('number','size__size','total_quantity')
    total_order_quantity = orders_qs.aggregate(total_quantity=Sum('quantity'))


    deliverys_qs = Delivery.objects.filter(job_no=job)
    deliverys = deliverys_qs.annotate(total_quantity=Sum('quantity')).values('number','date', 'size__size', 'total_quantity','piece_type__piece_type').order_by('number')


    deliverys_df = pd.DataFrame(deliverys)
    # print("DF : {}",deliverys_df)
    deliverys_df_pivot = deliverys_df.pivot(index=['number','date','piece_type__piece_type'],columns='size__size',values=['total_quantity'])
    deliverys_df_pivot_reset = deliverys_df_pivot.reset_index(drop=True)
    deliverys_df_pivot_dict = deliverys_df_pivot.to_dict()
    delivery_index = deliverys_df_pivot.index.tolist()
    delivery_columns = deliverys_df_pivot.columns.values.tolist()
    delivery_data =  deliverys_df_pivot.values.tolist()
    # print("DF PIVOT: {}",deliverys_df_pivot)
    # deliverys_json = deliverys_df_pivot.to_json(orient ='records')
    # print("DF PIVOT JSON: {}",deliverys_json)
    # deliverys_data = json.loads(deliverys_json)
    # print("DATA: {}",deliverys_data)
    # deliverys_list = [deliverys_df_pivot.columns.values.tolist()] +  deliverys_df_pivot.values.tolist()
    
    delivery_sizes = deliverys_qs.order_by().values('size__size').distinct()
    delivery_numbers = deliverys_qs.order_by().values('number','date','piece_type__piece_type').distinct()
    # delivery_list = list(Delivery.objects.filter(job_no=job).annotate(total_quantity=Sum('quantity')).values_list('number','date', 'size__size', 'total_quantity','piece_type__piece_type').order_by('number'))
    total_delivery_quantity = deliverys_qs.aggregate(total_quantity=Sum('quantity'))

    context = {}
    context['job'] = job
    context['orders'] = orders

    context['total_order_quantity'] = total_order_quantity
    context['deliverys'] = deliverys

    context['delivery_data'] = delivery_data
    context['delivery_sizes'] = delivery_sizes
    context['delivery_numbers'] = delivery_numbers
    # t_delivery_list = list(zip(*delivery_list))
    # context['t_delivery_list'] = t_delivery_list


    return render(request, 'production/jobs_detail.html', context)


# @login_required(login_url="/authentication/login/")
# def details_job(request, slug):
#     job = Job.objects.get(slug=slug)
#     orders_qs = Order.objects.filter(job_no=job)
#     orders = orders_qs.annotate(total_quantity=Sum('quantity')).values('number','size__size','total_quantity')
#     total_order_quantity = orders_qs.aggregate(total_quantity=Sum('quantity'))
#     orders_transposed = {}

#     for order in orders:
#         orders_transposed.setdefault(order['number'] ,{}).update(
#             {'SIZE-%s' % order['size__size']:order['total_quantity']}
#         )
  

#     deliverys_qs = Delivery.objects.filter(job_no=job)
#     deliverys = deliverys_qs.annotate(total_quantity=Sum('quantity')).values('number','date', 'size__size', 'total_quantity','piece_type__piece_type').order_by('number')
#     deliverys_transposed = {}
#     for delivery in deliverys:
#         deliverys_transposed.setdefault(delivery['number'] ,{}).update(
#             {'SIZE-%s' % delivery['size__size']:delivery['total_quantity']}
#         )
#         # delivery_data['number'] = delivery['number']
#         # delivery_data['date'] = delivery['date']
#         # delivery_data['size'] = delivery['size__size']
#         # delivery_data['quantity'] = delivery['total_quantity']
#         # delivery_data['piece_type'] = delivery['piece_type__piece_type']


#     # deliverys1 = Delivery.objects.filter(job_no=job).annotate(total_quantity=Sum('quantity')).values_list('number','date', 'size__size', 'total_quantity','piece_type__piece_type').order_by('number')

#     deliverys_df = pd.DataFrame(deliverys)
#     deliverys_df_pivot = deliverys_df.pivot(index=['number','date','piece_type__piece_type'],columns='size__size',values=['total_quantity'])
#     deliverys_list = [deliverys_df_pivot.columns.values.tolist()] +  deliverys_df_pivot.values.tolist()
    
#     delivery_sizes = deliverys_qs.order_by().values('size__size').distinct()
#     delivery_numbers = deliverys_qs.order_by().values('number','date','piece_type__piece_type').distinct()
#     # delivery_list = list(Delivery.objects.filter(job_no=job).annotate(total_quantity=Sum('quantity')).values_list('number','date', 'size__size', 'total_quantity','piece_type__piece_type').order_by('number'))
#     total_delivery_quantity = deliverys_qs.aggregate(total_quantity=Sum('quantity'))

#     context = {}
#     context['job'] = job
#     context['orders'] = orders
#     context['orders_transposed'] = orders_transposed
#     context['total_order_quantity'] = total_order_quantity
#     context['deliverys'] = deliverys
#     context['deliverys_transposed'] = deliverys_transposed
#     context['delivery_sizes'] = delivery_sizes
#     context['delivery_numbers'] = delivery_numbers
#     # t_delivery_list = list(zip(*delivery_list))
#     # context['t_delivery_list'] = t_delivery_list


#     return render(request, 'production/jobs_detail.html', context)


@login_required(login_url="/authentication/login/")
def add_delivery(request, slug):
    # DeliveryFormSet = inlineformset_factory(Job, Delivery, fields=('date','size', 'quantity',), can_delete=False, extra=6)
    DeliveryFormSet = formset_factory(DeliveryForm, extra=6, max_num=6, validate_min=True)
    context = {}
    msg = None
    job = Job.objects.get(slug=slug)
    context['job'] = job
    context['title'] = "Delivery"
   

    if request.method == 'GET':
        formset = DeliveryFormSet()
        context['formset'] = formset
        return render(request, 'production/add_delivery.html', context)

    if request.method == 'POST':
        formset = DeliveryFormSet(request.POST, request.FILES)
        delivery_number = increment_delivery_number() 

        if formset.is_valid():
            for inline_form in formset:
                if inline_form.cleaned_data:
                    delivery = inline_form.save(commit=False)
                    delivery.job_no = job  
                    delivery.number = delivery_number                
                    delivery.save()
                    messages.success(request, 'New Job has been Added')
                    msg = 'New Job has been Added'
            return redirect('production:jobs-list')
        else:
            messages.error(request, 'Problem processing your request')
            msg = 'Problem processing your request'
            return redirect('production:jobs-list')

    context['msg'] = msg
    return render(request, 'production/add_delivery.html', context) 

# @login_required(login_url="/authentication/login/")
# def add_delivery(request, slug):
#     DeliveryFormSet = inlineformset_factory(Job, Delivery, fields=('date','size', 'quantity',), can_delete=False, extra=6)
#     # OrderFormSet = formset_factory(OrderForm, extra=6, max_num=6, validate_min=True)
#     context = {}
#     msg = None
#     job = Job.objects.get(slug=slug)
#     context['job'] = job
#     context['title'] = "Delivery"
   

#     if request.method == 'GET':
#         formset = DeliveryFormSet(instance=job)
#         context['formset'] = formset
#         return render(request, 'production/add_delivery.html', context)

#     if request.method == 'POST':
#         formset = DeliveryFormSet(request.POST, request.FILES, instance=job)

#         if formset.is_valid():
#             for inline_form in formset:
#                 if inline_form.cleaned_data:
#                     delivery = inline_form.save(commit=False)
#                     delivery.job_no = job  
#                     delivery.number =  increment_delivery_number()                 
#                     delivery.save()
#                     messages.success(request, 'New Job has been Added')
#                     msg = 'New Job has been Added'
#             return redirect('production:jobs-list')
#         else:
#             messages.error(request, 'Problem processing your request')
#             msg = 'Problem processing your request'
#             return redirect('production:jobs-list')

#     context['msg'] = msg
#     return render(request, 'production/add_delivery.html', context)    