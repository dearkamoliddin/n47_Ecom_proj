from django.contrib import admin
from django.contrib.auth.models import User, Group
from app.models import Product, Image, Attribute, AttributeValue, ProductAttribute

# admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)


# admin.site.register(User)
# admin.site.unregister(Group)


class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'price')
    search_fields = ('name',)
    list_per_page = 2


admin.site.register(Product, ProductModelAdmin)
