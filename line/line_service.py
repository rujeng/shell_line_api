import json
from utils.http_request import HttpRequest

class Line():

    def __init__(self, *args, **kwargs):
        self.http_request = HttpRequest()
        return 
    
    def get_token(self, queries, client_id ,client_secret):
        url = "https://api.line.me/oauth2/v2.1/token"
        code = queries['code']
        channel_id = queries['channel_id']
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': f'https://6cdb-2405-9800-b600-a8ab-14d5-ab28-1b50-f372.ngrok.io/line/webhook?channel_id={channel_id}',
            'client_id': client_id,
            'client_secret': client_secret,
        }
        headers = {
            'Content-type':  "application/x-www-form-urlencoded"
        }
        print('data',data)
        return self.http_request.request('POST', url, data, headers)

    def get_profile(self, access_token):
        headers = {
            "Authorization": "Bearer "+ access_token
        }
        url = "https://api.line.me/v2/profile"
        return self.http_request.request('GET', url, None, headers)
    
    def notify(self, meta_dat, access_token):
        url = 'https://notify-api.line.me/api/notify'
        headers = {
            "Authorization": "Bearer "+ access_token,
            'Content-type':  "application/x-www-form-urlencoded"
        }
        data = meta_dat
        r  =self.http_request.request('POST', url ,data, headers)
        return r
    
    def push_message(self,user_id, meta_dat=None,channel_access_token = None):
        url = 'https://api.line.me/v2/bot/message/multicast'
        headers = {
            "Authorization": "Bearer "+ channel_access_token,
             'Content-Type':  "application/json"
        }
        data = { "to": [user_id],
                 "messages":[
        {
            "type":"text",
            "text": json.dumps(meta_dat)
        }]
        }
        r  =self.http_request.request('POST', url ,json.dumps(data), headers)
        return r