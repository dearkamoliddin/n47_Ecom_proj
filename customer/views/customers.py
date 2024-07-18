import csv
import json
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from customer.forms import CustomerModelForm, SendEmailForm
from customer.models import Customer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from conf.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage, get_connection
from django.conf import settings


# def send_email(request):
#     if request.method == "POST":
#         with get_connection(
#                 host=settings.EMAIL_HOST,
#                 port=settings.EMAIL_PORT,
#                 username=settings.EMAIL_HOST_USER,
#                 password=settings.EMAIL_HOST_PASSWORD,
#                 use_tls=settings.EMAIL_USE_TLS
#         ) as connection:
#             recipient_list = request.POST.get("email").split()
#             subject = request.POST.get("subject")
#             email_from = settings.EMAIL_HOST_USER
#             message = request.POST.get("message")
#             print(type(recipient_list))
#             EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
#
#     return render(request, 'customer/send_email.html')


def send_email(request):
    if request.method == "POST":
        with get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=settings.EMAIL_USE_TLS
        ) as connection:
            subject = request.POST.get("subject")
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST.get("email"), ]
            message = request.POST.get("message")
            EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
        return redirect("customer_l")

    return render(request, 'customer/send_email.html')


# def send_email(request):
#     if request.method == "POST":
#         with get_connection(
#                 host=settings.EMAIL_HOST,
#                 port=settings.EMAIL_PORT,
#                 username=settings.EMAIL_HOST_USER,
#                 password=settings.EMAIL_HOST_PASSWORD,
#                 use_tls=settings.EMAIL_USE_TLS
#         ) as connection:
#             subject = request.POST.get("subject")
#             email_from = settings.EMAIL_HOST_USER
#             recipient_list = [request.POST.get("email"), ]
#             message = request.POST.get("message")
#             EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
#         return redirect("customer_l")
#
#     return render(request, 'customer/send_email.html')


class CustomerListView(View):
    def get(self, request):
        page = request.GET.get('page')
        customers = Customer.objects.all().order_by('-id')
        paginator = Paginator(customers, 2)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context = {
            'page_obj': page_obj
        }
        return render(request, 'customer/customers.html', context)


# class CustomerDetailView(View):
#     def get(self, request, customer_id):
#         customer_det = Customer.objects.get(id=customer_id)
#         context = {
#             'customer_det': customer_det,
#         }
#         return render(request, 'customer/customer_details.html', context)


class CustomerDetailTemplateView(TemplateView):
    template_name = 'customer/customer_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(id=kwargs['customer_id'])
        context['customer'] = customer
        return context


class AddCustomerView(View):
    def get(self, request):
        form = CustomerModelForm()
        return render(request, 'customer/add-customer.html', {'form': form})

    def post(self, request):
        form = CustomerModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customer_l')
        return redirect('customer/add-customer.html')


# class EditCustomerView(View):
#     def get(self, request, customer_id):
#         customer = get_object_or_404(Customer, id=customer_id)
#         form = CustomerModelForm(instance=customer)
#         return render(request, 'customer/edit_customer.html', {'form': form})
#
#     def post(self, request, customer_id):
#         customer = get_object_or_404(Customer, id=customer_id)
#         form = CustomerModelForm(request.POST, instance=customer)
#         if form.is_valid():
#             form.save()
#             return redirect('customer_l')


class EditCustomerTemplateView(TemplateView):
    template_name = 'customer/edit_customer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(id=kwargs['customer_id'])
        context['form'] = CustomerModelForm(instance=customer)
        return context

    def post(self, request,  *args, **kwargs):
        context = self.get_context_data(**kwargs)
        customer = get_object_or_404(Customer, id=kwargs['customer_id'])
        form = CustomerModelForm(instance=customer, data=request.POST)
        context['form'] = form
        if form.is_valid():
            form.save()
            return redirect('customer_l')


class CustomerDeleteView(View):
    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        if customer:
            if customer.delete():
                messages.add_message(request, messages.SUCCESS, 'Customer successfully deleted')
            return redirect('customer_l')


class ExportCustomerView(View):
    def get(self, request):
        resource = CustomerResource()
        dataset = resource.export()

        if request.GET.get('format') == 'csv':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="my_model_data.csv"'
        elif request.GET.get('format') == 'xlsx':
            response = HttpResponse(dataset.xlsx,
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="my_model_data.xlsx"'
        elif request.GET.get('format') == 'json':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="my_model_data.json"'
        elif request.GET.get('format') == 'yaml':
            response = HttpResponse(dataset.yaml, content_type='application/x-yaml')
            response['Content-Disposition'] = 'attachment; filename="my_model_data.yaml"'
        else:
            return HttpResponseBadRequest("Unsupported format.")
        return response

    def render_to_response(self, context):
        return render(self.request, 'customer/customers.html', context)
