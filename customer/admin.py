from django.contrib import admin
from customer.models import Customer, CustomUser
from customer.forms import CustomUserModelForm
from import_export.admin import ImportExportModelAdmin

# admin.site.register(Customer)
# admin.site.register(CustomUser)


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone', 'email', 'is_active']
    search_fields = ['id', 'email']
    list_filter = ['joined', 'is_active']
    list_per_page = 2


@admin.register(CustomUser)
class CustomUserModelAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'birth_of_date', 'is_superuser']
    form = CustomUserModelForm

