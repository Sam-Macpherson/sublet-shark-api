import urllib

from model_bakery import baker
from rest_framework.test import APITestCase


class TestHelpers:
    """Useful testing helper functions."""

    @staticmethod
    def make_user(*args, **kwargs):
        user = baker.make('auth.User', *args, **kwargs)
        return user

    @staticmethod
    def add_query_params(path, **kwargs):
        return path + '?' + urllib.parse.urlencode(kwargs)


class SubletSharkAPITestCase(APITestCase, TestHelpers):
    pass
