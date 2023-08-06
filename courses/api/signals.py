from django.db.models.signals import pre_save
from django.dispatch import receiver
from courses.models import Author
from dateutil import relativedelta
from datetime import datetime


@receiver(pre_save, sender=Author)
def age_handler(sender, instance, **kwargs):
    instance.age = relativedelta.relativedelta(instance.date_Of_Birth, datetime.now())
