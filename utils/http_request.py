import requests
import json
from django.conf import settings

from line.tests import Test
from line.test_service import TestLine

class HttpRequest():

    def __init__(self, *args, **kwargs):
        # self.line = Line()
        # self.access_token = settings.access_token
        self.access_token = 'oxCyrrgf1jWuQFU7c6yBghkJDmmRhmvvDNN6xTHlb5i'
        return

    def request(self, method, url, data=None, headers=None, max_retires=3):
        res = requests.request(method, data=data, headers=headers, url=url)
        res = self.check_response(res)
        if max_retires <= 0:
            data = {
                'message': json.dumps(res)
            }
            # self.line.notify(data, settings.access_token)
            return res
        if res['ok'] == False:
            max_retires = max_retires - 1
            return self.request(method, url, data=None, headers=None, max_retires=max_retires)
        return res

    def check_response(self, response):
        if response.status_code >= 200 and response.status_code <= 302:
            return {'ok': True, 'result': response.json()}
        return {'ok': False, 'result': response.json()}