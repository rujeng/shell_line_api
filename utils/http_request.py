import time
import requests
import json
from django.conf import settings

from line import line_service

class HttpRequest():

    def __init__(self, *args, **kwargs):
        self.access_token = 'oxCyrrgf1jWuQFU7c6yBghkJDmmRhmvvDNN6xTHlb5i' #settings.access_token
        return

    def request(self, method, url, data=None, headers=None, max_retires=3):
        res = requests.request(method, data=data, headers=headers, url=url)
        res = self.check_response(res)
        if max_retires <= 0:
            return res
        if res['ok'] == False:
            time.sleep(5)
            max_retires = max_retires - 1
            line = line_service.Line()
            data = {
                'message': json.dumps(res)
            }
            line.notify(data, 'oxCyrrgf1jWuQFU7c6yBghkJDmmRhmvvDNN6xTHlb5i')
            #print('access ' , self.access_token)
            return self.request(method, url, data=None, headers=None, max_retires=max_retires)
        return res

    def check_response(self, response):
        if response.status_code >= 200 and response.status_code <= 302:
            return {'ok': True, 'result': response.json()}
        return {'ok': False, 'result': response.json()}