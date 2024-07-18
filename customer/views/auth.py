from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from customer.forms import LoginForm, RegisterModelForm, CustomerModelForm
from customer.models import Customer, CustomUser
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView, UpdateView, DeleteView
from customer.forms import LoginForm, RegisterModelForm
from django.contrib.auth.decorators import permission_required

from customer.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls.exceptions import NoReverseMatch


class CustomerLoginView(View):
    def login_page(request):
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(request, email=email, password=password)
                if user:
                    login(request, user)
                    return redirect('customer_l')
        else:
            form = LoginForm()

        return render(request, 'auth/login.html', {'form': form})


def logout_page(request):
    if request.method == 'POST':
        return redirect('logout')
    return render(request, 'auth/logout.html')


class LoginPageView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('customer_l')

        return render(request, 'auth/login.html', {'form': form})


class LoginPage(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True
    authentication_form = LoginForm

    def get_success_url(self):
        return reverse_lazy('customer_l')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Account activated')
        return redirect('customer_l')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('customer_l')


def activate_email(request, user, to_email):
    mail_subject = "Activate your account"
    message = render_to_string('customer/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"Dear {user}, pls go to your email {to_email} \
        inbox and click on received activation link to confirm your email.")
    else:
        message.error(request, "Sorry, Problem with your email is not verified.")


def register_page(request):
    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            activate_email(request, user, form.cleaned_data.get('email'))
            return redirect('customer_l')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = RegisterModelForm()
    return render(request, 'auth/register.html', {"form": form})




# class RegisterFormView(FormView):
#     template_name = 'auth/register.html'
#     form_class = RegisterModelForm
#     success_url = reverse_lazy('customer_l')
#
#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.is_active = False
#         user.email = form.cleaned_data['email']
#         user.password = form.cleaned_data['password']
#         user.save()
#         activate_email(form, user, form_class.cleaned_data.get('email'))
#         login(self.request, user)
#         # messages.success(self.request, 'Your account has been created!')
#         return redirect('customer_l')
