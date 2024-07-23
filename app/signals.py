import json

from conf.settings import BASE_DIR
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from app.models import Product
import os


@receiver(post_save, sender=Product)
def product_save(sender, instance, created, **kwargs):
    if created:
        print(f'{instance.name} is created')
        print(kwargs)
    else:
        print('Product is Updated')


post_save.connect(product_save, sender=Product)


@receiver(pre_delete, sender=Product)
def product_delete(sender, instance, **kwargs):
    product_data = {
        'id': instance.id,
        'name': instance.name,
        'price': instance.price,
        'description': instance.description,
    }
    file_path = os.path.join(BASE_DIR, f'app/deleted_products/{instance.name}.json')
    with open(file_path, mode='w') as file_json:
        json.dump(product_data, file_json, indent=4)

    print(f'{instance.name} is deleted')
