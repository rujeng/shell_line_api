import json
import time
import requests
import json
from django.conf import settings

class HttpRequest():

    def request(self, method, url, data=None, headers=None, max_retires=1):
        res = requests.request(method, data=data, headers=headers, url=url)
        res = self.check_response(res)
        if max_retires <= 0:
            line = Line()
            message = json.dumps(res)
            line.notify(message, 'oxCyrrgf1jWuQFU7c6yBghkJDmmRhmvvDNN6xTHlb5i')
            return res
        if res['ok'] == False:
            time.sleep(5)
            max_retires = max_retires - 1
            return self.request(method, url, data=None, headers=None, max_retires=max_retires)
        return res

    def check_response(self, response):
        if response.status_code >= 200 and response.status_code <= 302:
            return {'ok': True, 'result': response.json()}
        return {'ok': False, 'result': response.json()}

class Line(HttpRequest):

    def __init__(self, *args, **kwargs):
        return
    
    def get_token(self,code,branch_id, channel_id ,channel_secret):
        url = "https://api.line.me/oauth2/v2.1/token"
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': f'http://159.223.95.82/line/webhook?branch_id={branch_id}',
            'client_id': channel_id,
            'client_secret': channel_secret,
        }
        headers = {
            'Content-type':  "application/x-www-form-urlencoded"
        }
        return super().request('POST', url, data, headers)

    def get_profile(self, access_token):
        headers = {
            "Authorization": "Bearer "+ access_token
        }
        url = "https://api.line.me/v2/profile"
        return super().request('GET', url, None, headers)
    
    def notify(self, message, access_token):
        url = 'https://notify-api.line.me/api/notify'
        headers = {
            "Authorization": "Bearer "+ access_token,
            'Content-type':  "application/x-www-form-urlencoded"
        }
        data = {
                # 'message': json.dumps(message , ensure_ascii=False)
                'message': message
                # 'text': json.dumps(message , ensure_ascii=False)
        }
        return super().request('POST', url ,data, headers)
    
    def push_message(self, meta_dat=None,channel_access_token = None,message_data = None):
        url = 'https://api.line.me/v2/bot/message/push'
        headers = {
            "Authorization": "Bearer "+ channel_access_token,
             'Content-Type':  "application/json"
        }
        data = message_data
        return super().request('POST', url ,json.dumps(data), headers)

    def get_token_history(self,code, channel_id ,channel_secret,branch_id):
        url = "https://api.line.me/oauth2/v2.1/token"
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': f'http://159.223.95.82/line/webhistory?branch_id={branch_id}',
            'client_id': channel_id,
            'client_secret': channel_secret,
        }
        headers = {
            'Content-type':  "application/x-www-form-urlencoded"
        }
        return super().request('POST', url, data, headers)
