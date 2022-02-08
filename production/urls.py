from django.urls import path, re_path
from . import views

app_name = 'production'

urlpatterns = [

    path('jobs/list/', views.list_jobs, name='jobs-list'),
    path('jobs/edit/<slug:slug>',views.edit_jobs, name='jobs-edit'),
    path('jobs/add/delivery/<slug:slug>',views.add_delivery, name='jobs-add-delivery'),
    path('jobs/details/<slug:slug>',views.details_job, name='jobs-details'),


]