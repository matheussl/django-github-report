from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class Configuration(object):
    def __init__(self, **kwargs):
        pass

    def __getattr__(self, k):
        try:
            return getattr(settings, k)
        except AttributeError:
            raise ImproperlyConfigured("django-github-report requires %s setting." % k)

conf = Configuration()