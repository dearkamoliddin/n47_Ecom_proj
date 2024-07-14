from django.contrib import admin
from django.contrib.auth.models import User, Group
from import_export.admin import ImportExportModelAdmin
from app.models import Product, Image, Attribute, AttributeValue, ProductAttribute
from customer.models import Customer

# admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)


# admin.site.register(User)
# admin.site.unregister(Group)


class ProductModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'discount', 'price')
    search_fields = ('name',)
    list_per_page = 5


admin.site.register(Product, ProductModelAdmin)
