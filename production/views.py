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
import datetime

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
def add_jobs(request):
    # OrderFormSet = inlineformset_factory(Job, Order, fields=('id','size', 'quantity',), can_delete=False)
    FabricInwardFormSet = formset_factory(FabricInwardForm, extra=1)
    context = {}
    msg = None

    context['title'] = "Add Job"

    if request.method == 'GET':
        form = JobForm()
        formset = FabricInwardFormSet()

        context['form'] = form
        context['formset'] = formset
        return render(request, 'production/jobs_add.html', context)

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        formset = FabricInwardFormSet(request.POST, request.FILES)
        order_number = increment_inward_order_number()

        if all([form.is_valid(), formset.is_valid()]) :
            job = form.save()

            for inline_form in formset:
                if inline_form.cleaned_data:
                    inward_order = inline_form.save(commit=False)
                    inward_order.job_no = job 
                    inward_order.number = order_number                   
                    inward_order.save()
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
def list_jobs(request):
    # OrderFormSet = inlineformset_factory(Job, Order, fields=('id','size', 'quantity',), can_delete=False)
    FabricInwardFormSet = formset_factory(FabricInwardForm, extra=6, max_num=6, validate_min=True)
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
        formset = FabricInwardFormSet()

        context['form'] = form
        context['formset'] = formset
        return render(request, 'production/jobs_list.html', context)

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        formset = FabricInwardFormSet(request.POST, request.FILES)
        order_number = increment_inward_order_number()

        if all([form.is_valid(), formset.is_valid()]) :
            job = form.save()
            for inline_form in formset:
                if inline_form.cleaned_data:
                    inward_order = inline_form.save(commit=False)
                    inward_order.job_no = job 
                    inward_order.number = order_number                   
                    inward_order.save()
                    messages.success(request, 'New Job has been Added')
                    msg = 'New Job has been Added'
            return redirect('production:jobs-list')
        else:
            messages.error(request, 'Problem processing your request')
            msg = 'Problem processing your request'
            return redirect('production:jobs-list')

    context['msg'] = msg
    return render(request, 'production/jobs_list.html', context)


# @login_required(login_url="/authentication/login/")
# def list_jobs(request):
#     # OrderFormSet = inlineformset_factory(Job, Order, fields=('id','size', 'quantity',), can_delete=False)
#     OrderFormSet = formset_factory(OrderForm, extra=6, max_num=6, validate_min=True)
#     context = {}
#     msg = None
#     jobs = Job.objects.all()
    
#     # order_summary= order_data.values('job_no','job_no__date','job_no__status','job_no__color','job_no__style').annotate(total_qty=Sum('quantity'))
#     MyJobFilter = JobFilter(request.GET, queryset=jobs)

#     jobs = MyJobFilter.qs

#     context['jobs'] = jobs

#     context['MyJobFilter'] = MyJobFilter
#     context['title'] = "Add Job"

#     if request.method == 'GET':
#         form = JobForm()
#         formset = OrderFormSet()

#         context['form'] = form
#         context['formset'] = formset
#         return render(request, 'production/jobs_list.html', context)

#     if request.method == 'POST':
#         form = JobForm(request.POST, request.FILES)
#         formset = OrderFormSet(request.POST, request.FILES)
#         order_number = increment_order_number()

#         if all([form.is_valid(), formset.is_valid()]) :
#             job = form.save()
#             for inline_form in formset:
#                 if inline_form.cleaned_data:
#                     order = inline_form.save(commit=False)
#                     order.job_no = job 
#                     order.number = order_number                   
#                     order.save()
#                     messages.success(request, 'New Job has been Added')
#                     msg = 'New Job has been Added'
#             return redirect('production:jobs-list')
#         else:
#             messages.error(request, 'Problem processing your request')
#             msg = 'Problem processing your request'
#             return redirect('production:jobs-list')

#     context['msg'] = msg
#     return render(request, 'production/jobs_list.html', context)

@login_required(login_url="/authentication/login/")
def edit_jobs(request, slug):
    # FabricInwardFormSet = formset_factory(FabricInwardForm, extra=1)
    # FabricInwardFormSet = inlineformset_factory(Job, FabricInward, fields=('color', 'fabric_type','no_of_rolls','dc_weight','received_weight',), can_delete=False, extra=0)
    FabricInwardFormSet = inlineformset_factory(Job, FabricInward, FabricInwardForm, can_delete=False, extra=0)

    # OrderFormSet = formset_factory(OrderForm, extra=6, max_num=6, validate_min=True)
    context = {}
    msg = None
    job = Job.objects.get(slug=slug)
    context['title'] = "Edit Job"

    if request.method == 'GET':
        form = JobForm(instance=job)
        formset = FabricInwardFormSet(instance=job)

        context['form'] = form
        context['formset'] = formset
        return render(request, 'production/jobs_edit.html', context)

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES, instance=job)
        formset = FabricInwardFormSet(request.POST, request.FILES, instance=job)

        if formset.is_valid():
            if form.is_valid():
                job = form.save()
            for inline_form in formset:
                if inline_form.cleaned_data:
                    inward_order = inline_form.save(commit=False)
                    inward_order.job_no = job  
                    # order.number =  increment_order_number()                  
                    inward_order.save()
            messages.success(request, 'Job has been Updated')
            msg = 'Job has been Updated'
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


    transposed_order_data = {}
    order_data_measure_columns_types = {}
    order_data_measure_columns = []
    for order in orders:
        transposed_order_data.setdefault(order['number'], {}).update(
                        {'Size-%s' % order['size__size']: order['total_quantity']})
        order_data_measure_columns_types['Size-%s' % order['size__size']] = 'int64'
        order_data_measure_columns.append('Size-%s' % order['size__size'])

    order_data_measure_columns = list(set(order_data_measure_columns))
    order_df = pd.DataFrame(transposed_order_data).fillna(0)
    order_data_df_reset = order_df.transpose().reset_index().rename(columns={'index': 'order #'})
    # order_data_df = order_data_df_reset.astype({'Size-S': 'int32','Size-L': 'int32'})
    order_data_df = order_data_df_reset.astype(order_data_measure_columns_types)

    print(order_data_df.dtypes)
    order_data_df['total qty'] = order_data_df.sum(axis=1, numeric_only=True)
    order_data_measure_columns.append('total qty')
    order_data_measure_columns_types['total qty'] = 'int64'
    order_data_df.loc['total'] = order_data_df[order_data_measure_columns].sum()
    order_data_df = order_data_df.fillna('').astype(order_data_measure_columns_types)
    order_data_columns = order_data_df.columns.values.tolist()
    order_data_rows = order_data_df.values.tolist()
    print("Columns: {}", order_data_columns)
    print("Rows: {}", order_data_rows)

    deliverys_qs = Delivery.objects.filter(job_no=job)
    deliverys = deliverys_qs.annotate(total_quantity=Sum('quantity')).values('number','date', 'size__size', 'total_quantity','piece_type__piece_type').order_by('number')

    transposed_delivery_data = {}
    delivery_data_measure_columns_type = {}
    delivery_data_measure_columns = []
    for delivery in deliverys:
        transposed_delivery_data.setdefault(delivery['number'], {}).update(
                        {'date' : delivery['date'], 'piece type' : delivery['piece_type__piece_type'], 'Size-%s' % delivery['size__size']: delivery['total_quantity']})
        delivery_data_measure_columns_type['Size-%s' % delivery['size__size']] = 'int64'
        delivery_data_measure_columns.append('Size-%s' % delivery['size__size']) 

    delivery_data_measure_columns = list(set(delivery_data_measure_columns))
    delivery_df = pd.DataFrame(transposed_delivery_data).fillna(0)
    delivery_df_reset = delivery_df.transpose().reset_index().rename(columns={'index': 'delivery #'})    
    delivery_data_df = delivery_df_reset.astype(delivery_data_measure_columns_type)

    print(delivery_data_df.dtypes)
    delivery_data_df['total qty'] = delivery_data_df.sum(axis=1, numeric_only=True)
    delivery_data_measure_columns.append('total qty')
    delivery_data_measure_columns_type['total qty'] = 'int64'
    delivery_data_df.loc['total'] = delivery_data_df[delivery_data_measure_columns].sum()
    delivery_data_df = delivery_data_df.fillna('').astype(delivery_data_measure_columns_type)
    delivery_data_columns = delivery_data_df.columns.values.tolist()
    delivery_data_rows = delivery_data_df.values.tolist()
    print("Columns: {}", delivery_data_columns)
    print("Rows: {}", delivery_data_rows)    

    balance_data_df = order_data_df[order_data_measure_columns] - delivery_data_df[delivery_data_measure_columns]
    balance_data_df = balance_data_df.fillna('')
    balance_data_columns = balance_data_df.columns.values.tolist()
    balance_data_rows = balance_data_df.loc['total'].values.tolist()

    context = {}
    context['job'] = job
    context['order_data_columns'] = order_data_columns
    context['order_data_rows'] = order_data_rows
    context['delivery_data_columns'] = delivery_data_columns
    context['delivery_data_rows'] = delivery_data_rows    
    context['balance_data_columns'] = balance_data_columns
    context['balance_data_rows'] = balance_data_rows 

    return render(request, 'production/jobs_detail.html', context)


@login_required(login_url="/authentication/login/")
def add_order(request, slug):
    # DeliveryFormSet = inlineformset_factory(Job, Delivery, fields=('date','size', 'quantity',), can_delete=False, extra=6)
    OrderFormSet = formset_factory(OrderForm, extra=1)
    context = {}
    msg = None
    job = Job.objects.get(slug=slug)
    context['job'] = job
    context['title'] = "Order"
   

    if request.method == 'GET':
        formset = OrderFormSet()
        context['formset'] = formset
        return render(request, 'production/order_add.html', context)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, request.FILES)
        order_number = increment_order_number() 

        if formset.is_valid():
            for inline_form in formset:
                if inline_form.cleaned_data:
                    order = inline_form.save(commit=False)
                    order.job_no = job  
                    order.number = order_number                
                    order.save()
                    messages.success(request, 'New Order has been Added')
                    msg = 'New Order has been Added'
            return redirect('production:jobs-list')
        else:
            messages.error(request, 'Problem processing your request')
            msg = 'Problem processing your request'
            return redirect('production:jobs-list')

    context['msg'] = msg
    return render(request, 'production/order_add.html', context)


@login_required(login_url="/authentication/login/")
def list_deliveries(request):
    # OrderFormSet = inlineformset_factory(Job, Order, fields=('id','size', 'quantity',), can_delete=False)

    context = {}
    msg = None
    
    deliveries_qs = Delivery.objects.all()

    # order_summary= order_data.values('job_no','job_no__date','job_no__status','job_no__color','job_no__style').annotate(total_qty=Sum('quantity'))
    MyDeliveryFilter = DeliveryFilter(request.GET, queryset=deliveries_qs)

    deliveries = MyDeliveryFilter.qs

    
    deliveries = deliveries.annotate(total_quantity=Sum('quantity')).values('number','job_no','date', 'size__size', 'total_quantity').order_by('number')

    transposed_delivery_data = {}
    delivery_data_measure_columns_type = {}
    delivery_data_measure_columns = []
    for delivery in deliveries:
        transposed_delivery_data.setdefault(delivery['number'], {}).update(
                        {'job #' : delivery['job_no'], 'date' : delivery['date'], 'Size-%s' % delivery['size__size']: delivery['total_quantity']})
        delivery_data_measure_columns_type['Size-%s' % delivery['size__size']] = 'int64'
        delivery_data_measure_columns.append('Size-%s' % delivery['size__size']) 

    delivery_data_measure_columns = list(set(delivery_data_measure_columns))
    delivery_df = pd.DataFrame(transposed_delivery_data).fillna(0)
    delivery_df_reset = delivery_df.transpose().reset_index().rename(columns={'index': 'delivery #'})    
    delivery_data_df = delivery_df_reset.astype(delivery_data_measure_columns_type)

    print(delivery_data_df.dtypes)
    delivery_data_df['total qty'] = delivery_data_df.sum(axis=1, numeric_only=True)
    delivery_data_measure_columns.append('total qty')
    delivery_data_measure_columns_type['total qty'] = 'int64'
    delivery_data_df.loc['total'] = delivery_data_df[delivery_data_measure_columns].sum()
    delivery_data_df = delivery_data_df.fillna('').astype(delivery_data_measure_columns_type)
    delivery_data_columns = delivery_data_df.columns.values.tolist()
    delivery_data_rows = delivery_data_df.values.tolist()
    print("Columns: {}", delivery_data_columns)
    print("Rows: {}", delivery_data_rows)     

    context['delivery_data_columns'] = delivery_data_columns
    context['delivery_data_rows'] = delivery_data_rows  

    context['MyDeliveryFilter'] = MyDeliveryFilter
    context['title'] = "Deliveries"

    context['msg'] = msg
    return render(request, 'production/deliveries_list.html', context)

@login_required(login_url="/authentication/login/")
def summary_deliveries(request):
 
    context = {}
    msg = None
    
    deliveries_qs = Delivery.objects.all()

    # order_summary= order_data.values('job_no','job_no__date','job_no__status','job_no__color','job_no__style').annotate(total_qty=Sum('quantity'))
    MyDeliveryFilter = DeliveryFilter(request.GET, queryset=deliveries_qs)

    deliveries = MyDeliveryFilter.qs

    
    deliveries = deliveries.annotate(total_quantity=Sum('quantity')).values('number','job_no','date', 'size__size', 'total_quantity').order_by('number')

    transposed_delivery_data = {}
    delivery_data_measure_columns_type = {}
    delivery_data_measure_columns = []
    for delivery in deliveries:
        transposed_delivery_data.setdefault(delivery['number'], {}).update(
                        {'job #' : delivery['job_no'], 'date' : delivery['date'], 'Size-%s' % delivery['size__size']: delivery['total_quantity']})
        delivery_data_measure_columns_type['Size-%s' % delivery['size__size']] = 'int64'
        delivery_data_measure_columns.append('Size-%s' % delivery['size__size']) 

    delivery_data_measure_columns = list(set(delivery_data_measure_columns))
    delivery_df = pd.DataFrame(transposed_delivery_data).fillna(0)
    delivery_df_reset = delivery_df.transpose().reset_index().rename(columns={'index': 'delivery #'})    
    delivery_data_df = delivery_df_reset.astype(delivery_data_measure_columns_type)

    print(delivery_data_df.dtypes)
    delivery_data_df['total qty'] = delivery_data_df.sum(axis=1, numeric_only=True)
    delivery_data_measure_columns.append('total qty')
    delivery_data_measure_columns_type['total qty'] = 'int64'
    delivery_data_df.loc['total'] = delivery_data_df[delivery_data_measure_columns].sum()
    delivery_data_df = delivery_data_df.fillna('').astype(delivery_data_measure_columns_type)
    delivery_data_columns = delivery_data_df.columns.values.tolist()
    delivery_data_rows = delivery_data_df.values.tolist()
    print("Columns: {}", delivery_data_columns)
    print("Rows: {}", delivery_data_rows)     

    context['delivery_data_columns'] = delivery_data_columns
    context['delivery_data_rows'] = delivery_data_rows  

    context['MyDeliveryFilter'] = MyDeliveryFilter
    context['title'] = "Deliveries"

    context['msg'] = msg
    return render(request, 'production/deliveries_summary.html', context)


@login_required(login_url="/authentication/login/")
def add_delivery(request, slug=None):
    job = Job.objects.get(slug=slug)
    # order_size_list = Order.objects.filter(job_no=job).order_by('size').distinct('size')
    order_size_list = Order.objects.filter(job_no=job).order_by('size').distinct()


    # DeliveryFormSet = inlineformset_factory(Job, Delivery, fields=('date','size', 'quantity',), can_delete=False, extra=6)
    # DeliveryFormSet = formset_factory(DeliveryForm, extra=(len(order_size_list))-1)
    DeliveryFormSet = formset_factory(DeliveryForm, extra=0)

    context = {}
    msg = None
    
    piecetype_list = PieceType.objects.all()
    context['job'] = job
    context['piecetype_list'] = piecetype_list
    context['title'] = "Delivery"
    initial = []
    size_list = []
    for item in order_size_list:
        if item.size not in  size_list:
            size_list.append(item.size)
            initial.append({'size':item.size})

    if request.method == 'GET':
        formset = DeliveryFormSet(initial=initial)
        context['formset'] = formset
        return render(request, 'production/delivery_add.html', context)

    if request.method == 'POST':
        formset = DeliveryFormSet(request.POST, request.FILES)
        delivery_number = increment_delivery_number() 
        piece_type_pk = request.POST.get('piecetype_pk')
        piece_type = PieceType.objects.get(pk=piece_type_pk)

        if formset.is_valid():
            for inline_form in formset:
                if inline_form.cleaned_data:
                    delivery = inline_form.save(commit=False)
                    delivery.job_no = job  
                    delivery.number = delivery_number  
                    delivery.piece_type = piece_type              
                    delivery.save()
                    messages.success(request, 'New Delivery has been Added')
                    msg = 'New Delivery has been Added'
            return redirect('production:jobs-list')
        else:
            messages.error(request, 'Problem processing your request')
            msg = 'Problem processing your request'
            return redirect('production:jobs-list')

    context['msg'] = msg
    return render(request, 'production/delivery_add.html', context) 

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