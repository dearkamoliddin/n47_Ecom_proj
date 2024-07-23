import os
import json
from conf.settings import BASE_DIR
from customer.models import Customer
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete


@receiver(post_save, sender=Customer)
def user_save(sender, instance, created, **kwargs):
    if created:
        print(f'{instance.name} is created')
        print(kwargs)

        from django.core.mail import send_mail

        send_mail(
            "Subject here, Hi",
            "Welcome!",
            "dearkamoliddin@gmail.com",
            ["dearkamoliddin@gmail.com"],
            fail_silently=False,
        )


    else:
        print('Product is problem')


post_save.connect(user_save, sender=Customer)


@receiver(pre_save, sender=Customer)
def customer_save(sender, instance, **kwargs):
    customer_data = {
        'id': instance.id,
        'full_name': instance.full_name,
        'email': instance.email,
        'phone': instance.phone,
        'address': instance.address,
    }
    file_path = os.path.join(BASE_DIR, f'customer/saved_customers/{instance.full_name}.txt')
    with open(file_path, mode='w') as file:
        json.dump(customer_data, file, indent=4)

    print(f'{instance.full_name} is saved')


@receiver(pre_delete, sender=Customer)
def customer_save(sender, instance, **kwargs):
    customer_data = {
        'id': instance.id,
        'full_name': instance.full_name,
        'email': instance.email,
        'phone': instance.phone,
        'address': instance.address,
    }
    file_path = os.path.join(BASE_DIR, f'customer/deleted_customers/{instance.full_name}.txt')
    with open(file_path, mode='w') as file:
        json.dump(customer_data, file, indent=4)

    print(f'{instance.full_name} is deleted')

