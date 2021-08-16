import urllib

from model_bakery import baker
from rest_framework.test import APITestCase

from subletshark import settings


class TestHelpers:
    """Useful testing helper functions."""

    @staticmethod
    def make_user(*args, **kwargs):
        user = baker.make(settings.AUTH_USER_MODEL, *args, **kwargs)
        return user

    @staticmethod
    def add_query_params(path, **kwargs):
        return path + '?' + urllib.parse.urlencode(kwargs)


class SubletSharkAPITestCase(APITestCase, TestHelpers):
    pass
