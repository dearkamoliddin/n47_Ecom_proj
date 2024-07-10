from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from customer.forms import CustomerModelForm
from customer.models import Customer
from django.core.paginator import Paginator


def customers(request):
    customer_list = Customer.objects.all()
    p = Paginator(customer_list, 2)
    page_num = request.GET.get('page')
    page_obj = p.get_page(page_num)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'customer/customers.html', context)


def customer_detail(request, customer_id):
    customer_det = Customer.objects.get(id=customer_id)
    context = {
        'customer_det': customer_det,
    }
    return render(request, 'customer/customer_details.html', context)


def add_customer(request):
    form = CustomerModelForm()
    if request.method == 'POST':
        form = CustomerModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customer')

    context = {
        'form': form,
    }

    return render(request, 'customer/add-customer.html', context)


def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if customer:
        customer.delete()
        messages.add_message(
            request,
            messages.SUCCESS,
            'Customer successfully deleted'
        )
        return redirect('customer')


def edit_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerModelForm(instance=customer)
    if request.method == 'POST':
        form = CustomerModelForm(instance=customer, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customer')
    context = {
        'form': form,
    }
    return render(request, 'customer/edit_customer.html', context)

