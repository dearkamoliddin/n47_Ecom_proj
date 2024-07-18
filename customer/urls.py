from django.urls import path, include
from customer.views.auth import logout_page, LoginPage, LoginPageView, register_page, activate_email, activate
from customer.views.customers import (
    CustomerListView,
    CustomerDetailTemplateView,
    AddCustomerView,
    EditCustomerTemplateView,
    CustomerDeleteView,
    ExportCustomerView, send_email,
)

urlpatterns = [
    path('customer_list/', CustomerListView.as_view(), name='customer_l'),
    path('customer_detail/<int:customer_id>/', CustomerDetailTemplateView.as_view(), name='customer_detail'),
    path('add-customer/', AddCustomerView.as_view(), name='add_customer'),
    path('edit_customer/<int:customer_id>/', EditCustomerTemplateView.as_view(), name='edit_customer'),
    path('customer_delete/<int:customer_id>/', CustomerDeleteView.as_view(), name='customer_delete'),
    path('send_email/', send_email, name='send_email'),



    # Authentication path
    path('login_page/', LoginPage.as_view(), name='login'),
    path('logout_page/', logout_page, name='logout'),
    path('register/', register_page, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('export-data/', ExportCustomerView.as_view(), name='export_data'),
]
