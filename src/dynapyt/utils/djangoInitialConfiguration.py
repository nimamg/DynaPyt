import os

from .initialConfiguration import BaseInitialConfiguration


class DjangoConfiguration(BaseInitialConfiguration):
    def setup(self, *args, **kwargs):
        if os.environ.get('DJANGO_SETTINGS_MODULE', None) is None:
            raise ValueError('The DJANGO_SETTINGS_MODULE environment variable is not defined')
        try:
            import django
            django.setup()
        except ImportError as e:
            print('Django could not be imported,', e)
            raise e
        except Exception as e:
            print('Exception occurred while setting up Django settings,', e)
            raise e