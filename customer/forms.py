from django import forms
from customer.authentication import  AuthenticationForm
from customer.models import Customer, CustomUser
from django.contrib.auth.models import Permission


class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ()


class SendEmailForm(forms.Form):
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    from_user = forms.EmailField()
    to = forms.EmailField()


class LoginForm(AuthenticationForm):
    email = forms.EmailField()
    password = forms.CharField(max_length=255)

    def clean_email(self):
        email = self.data.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email does not exist')
        return email

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.data.get('password')
        try:
            user = CustomUser.objects.get(email=email)
            print(user)
            if not user.check_password(password):
                raise forms.ValidationError('Password did not match')
        except CustomUser.DoesNotExist:
            raise forms.ValidationError(f'{email} do not exists')
        return password


class RegisterModelForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=255)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(f'The {email} is already registered')
        return email

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password did not match')
        return password


class CustomUserModelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        exclude = ()


EXPORT_FORMAT_CHOICES = [
    ('csv', 'CSV'),
    ('xlsx', 'Excel'),
    ('json', 'JSON'),
]


class ExportForm(forms.Form):
    export_format = forms.ChoiceField(choices=EXPORT_FORMAT_CHOICES)


class ImportForm(forms.Form):
    import_format = forms.ChoiceField(choices=EXPORT_FORMAT_CHOICES)
