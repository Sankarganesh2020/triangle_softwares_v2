from django.urls import path, re_path
from . import views

app_name = 'production'

urlpatterns = [

    path('jobs/list/', views.list_jobs, name='jobs-list'),
    path('jobs/add/', views.add_jobs, name='jobs-add'),
    path('jobs/edit/<slug:slug>',views.edit_jobs, name='jobs-edit'),
    path('jobs/add/order/<slug:slug>',views.add_order, name='jobs-add-order'),
    path('jobs/add/delivery/<slug:slug>',views.add_delivery, name='jobs-add-delivery'),
    path('jobs/details/<slug:slug>',views.details_job, name='jobs-details'),
    path('deliveries/list/', views.list_deliveries, name='deliveries-list'),
    # path('deliveries/summary/', views.summary_deliveries, name='deliveries-summary'),

]