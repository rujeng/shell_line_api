import json

from requests.models import codes
from line.line_service import HttpRequest
from otp.models import OtpRequest

class Otp(HttpRequest):

    def __init__(self, *args, **kwargs):
        return
    
    def get_otp(self,mobile_no):
        url = "https://portal-otp.smsmkt.com/api/otp-send"
        headers = {
            "Content-Type": "application/json",
            "api_key": "0493ae1e4eec4ec1e70ae3b065dfaf26",
            "secret_key": "xn81kOQjOS1J4dzO"
        }
        data = {
            "project_key" : "07724f9a1e",
            "phone": f"{mobile_no}",
            "ref_code":""
        }
        return super().request('POST', url ,json.dumps(data), headers)
    
    def verify_otp(self,token,otp_code):
        url = "https://portal-otp.smsmkt.com/api/otp-validate"
        headers = {
            "Content-Type": "application/json",
            "api_key": "0493ae1e4eec4ec1e70ae3b065dfaf26",
            "secret_key": "xn81kOQjOS1J4dzO"
        }
        data = {
            "token": f"{token}",
            "otp_code": f"{otp_code}",
            "ref_code": ""
        }
        return super().request('POST', url ,json.dumps(data), headers)
    
    def register_get_otp(self,line_id,mobile_no,full_name):      
        # otp_result = {'ok': True, 'result':{
        #     "code": "000",
        #     "detail": "OK.",
        #     "result": {
        #         "token": "6c680d5c-9494-4e60-8a96-24bef609efda",
        #         "ref_code": "383451"
        #             }
        #     }}
        otp_result = self.get_otp(mobile_no)
        print('otp_result ' , otp_result )
        if otp_result['ok'] and otp_result['result']['code'] == '000':
            token = otp_result['result']['result']['token']
            ref_code = otp_result['result']['result']['ref_code']
            meta_data = {'line_id': line_id ,'full_name': full_name, 'mobile_no': mobile_no,'token':token,'ref_code':ref_code}
            self.__save_otp_with_line_id(meta_data)
            # can get token : "xxxx" , ref_code : ""
            return True,ref_code
        return False,''

    def __save_otp_with_line_id(self,meta_data):
        line_id=meta_data['line_id']
        mobile_no = meta_data['mobile_no']
        token = meta_data['token']
        ref_code = meta_data['ref_code']
        full_name = meta_data['full_name']
        otp_request_create = OtpRequest.objects.create(line_id=line_id,full_name=full_name,mobile_no=mobile_no,token=token,ref_code=ref_code)
        return otp_request_create
        
    def register_verify_otp(self,line_id,otp_code):
        otp_request = OtpRequest.objects.filter(line_id=line_id).order_by('-id').first()
        if otp_request.count > 3:
            return False,'otp is over 3 times please get otp again.', otp_request
        token = otp_request.token
        otp_result = self.verify_otp(token,otp_code)
        if otp_result['ok'] and otp_result['result']['code'] == '000':
            if otp_result['result']['result']['status']:
                
                return True,'',otp_request
            else:
                otp_request.count += 1
                otp_request.save()
                return False,'Wrong Password',otp_request
        return False,'Error occurred',otp_request # Condition error เพิ่ม
         

    
