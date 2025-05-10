from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ProductInstance
from django.utils.deprecation import MiddlewareMixin
from threading import local

# Thread local storage to store the current user
_thread_locals = local()


def get_current_user():
    """
    Returns the current user from the thread local storage.
    """
    return getattr(_thread_locals, 'user', None)


class CurrentUserMiddleware(MiddlewareMixin):
    """
    Middleware that stores the current user in thread local storage.
    """
    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)


@receiver(pre_save, sender=ProductInstance)
def set_product_user(sender, instance, **kwargs):
    """
    Signal to automatically set the user field of a ProductInstance 
    to the current user if it's not already set.
    """
    if instance.user is None:
        current_user = get_current_user()
        if current_user and current_user.is_authenticated:
            instance.user = current_user 