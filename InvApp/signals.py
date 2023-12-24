from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model

from .models import Notice

User = get_user_model()

@receiver(post_save, sender=Notice)
def send_notice_email(sender, instance, created, **kwargs):
    if created:
        subject = 'New notice created!'
        message = 'Has A New Notice: {}'.format(instance.title)
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email for user in User.objects.all()]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
