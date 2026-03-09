from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from holly import views

urlpatterns =[
    
    path('', views.home, name='home'),
    path('step2/', views.step2, name='step2'),

                 
    path('admin-login/', views.admin_login, name='admin_login'),
    path('custom-admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-floorplans/', views.admin_floorplans, name='admin_floorplans'),
    path('admin-kitchen/', views.admin_kitchen, name='admin_kitchen'),
    path('admin-accessories/', views.admin_accessories, name='admin_accessories'),

                  
    path('admin-modules/<str:category>/', views.admin_modules, name='admin_modules'),
    path('api/submit-enquiry/', views.submit_enquiry, name='submit_enquiry'),
    path('api/delete-enquiry/<int:id>/', views.delete_enquiry, name='delete_enquiry'),
    path('api/update-enquiry/<int:id>/', views.update_enquiry, name='update_enquiry'),
    path('api/add-floorplan/', views.add_floorplan, name='add_floorplan'),
    path('api/delete-floorplan/<int:id>/', views.delete_floorplan, name='delete_floorplan'),

    path('api/add-kitchen/', views.add_kitchen, name='add_kitchen'),
    path('api/delete-kitchen/<int:id>/', views.delete_kitchen, name='delete_kitchen'),
    path('api/add-accessory/', views.add_accessory, name='add_accessory'),
    path('api/delete-accessory/<int:id>/', views.delete_accessory, name='delete_accessory'),
    path('api/add-module/', views.add_module, name='add_module'),
    path('api/delete-module/<int:id>/', views.delete_module, name='delete_module'),

    path('invoice/<int:id>/', views.enquiry_invoice, name='enquiry_invoice'),

    path('api/update-kitchen/<int:id>/', views.update_kitchen, name='update_kitchen'),
    path('api/update-accessory/<int:id>/', views.update_accessory, name='update_accessory'),
    path('api/update-module/<int:id>/', views.update_module, name='update_module'),
    path('api/update-floorplan/<int:id>/', views.update_floorplan, name='update_floorplan'),
]