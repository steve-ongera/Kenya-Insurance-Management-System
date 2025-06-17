from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('customers/', views.CustomerListView.as_view(), name='customer-list'),
    path('customers/edit/<uuid:customer_id>/', views.edit_customer, name='edit-customer'),
    path('customers/<uuid:customer_uuid>/', views.customer_detail, name='customer_detail'),
    path('customers/add/', views.add_customer, name='add-customer'),
    path('customers/search/', views.search_customers, name='search-customers'),

]
