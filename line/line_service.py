import json
from utils.http_request import HttpRequest

class Line(HttpRequest):

    def __init__(self, *args, **kwargs):
        return
    
    def get_token(self,code,branch_id, channel_id ,channel_secret):
        url = "https://api.line.me/oauth2/v2.1/token"
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': f'https://507e-2405-9800-b600-cbe-29dd-f2f4-900-9241.ngrok.io/line/webhook?branch_id={branch_id}',
            'client_id': channel_id,
            'client_secret': channel_secret,
        }
        headers = {
            'Content-type':  "application/x-www-form-urlencoded"
        }
        print('data',data)
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