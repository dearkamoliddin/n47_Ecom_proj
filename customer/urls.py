from django.urls import path
from customer.views.auth import login_page, logout_page, register_page
from customer.views.customers import customers, customer_detail, add_customer, delete_customer, edit_customer

urlpatterns = [
    path('customer/', customers, name='customer_l'),
    path('add-customer/', add_customer, name='add_customer'),
    path('customer/<int:customer_id>/', customer_detail, name='customer_detail'),
    path('customer/<int:pk>/delete', delete_customer, name='delete_customer'),
    path('customer/<int:pk>/edit', edit_customer, name='edit'),
    # Authentication path
    path('login_page/', login_page, name='login'),
    path('logout_page/', logout_page, name='logout'),
    path('register/', register_page, name='register'),
]
