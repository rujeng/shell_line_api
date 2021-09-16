from utils.http_request import HttpRequest

class Line():

    def __init__(self, *args, **kwargs):
        self.http_request = HttpRequest()
        return 
    
    def get_token(self, queries):
        url = "https://api.line.me/oauth2/v2.1/token"
        code = queries['code']
        channalId = queries['channalId']
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': f'https://0ec5-2405-9800-b600-3ed0-f044-8f4c-b94f-ebed.ngrok.io/linehook?channel={channalId}',
            'client_id': "1656347890",
            'client_secret': "98e7519ad012131dc5d34fbebf87a612",
        }
        headers = {
            'Content-type':  "application/x-www-form-urlencoded"
        }
        r = self.http_request.request('POST', url, data, headers)
        print(r)

    def get_profile(self, access_token):
        headers = {
            "Authorization": "Bearer "+ access_token
        }
        url = "https://api.line.me/v2/profile"
        r = self.http_request.request('GET', url, None, headers)
        print(r)
    
    def notify(self, meta_dat, access_token):
        url = 'https://notify-api.line.me/api/notify'
        headers = {
            "Authorization": "Bearer "+ access_token,
            'Content-type':  "application/x-www-form-urlencoded"
        }
        data = meta_dat
        r  =self.http_request.request('POST', url ,data, headers)
        return r