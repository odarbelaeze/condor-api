import json
import pytest

from sanic.testing import SanicTestClient


class DecoratedResponse(object):
    def __init__(self, response):
        self._response = response
    def json(self):
        return json.loads(self._response.body.decode('utf-8'))
    def __getattr__(self, name):
        return getattr(self._response, name)


class WrappedSanicTestClient(SanicTestClient):
    def _sanic_endpoint_test(self, *args, **kwargs):
        req, res = super()._sanic_endpoint_test(*args, **kwargs)
        return req, DecoratedResponse(res)



@pytest.fixture()
def client():
    from app import app
    return WrappedSanicTestClient(app)
