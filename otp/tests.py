from django.test import TestCase
from unittest import mock
from otp.otp_service import Otp
from otp.models import OtpRequest

def mock_get_otp(mobile):
    result = {'ok': True, 'result':{
            "code": "000",
            "detail": "OK.",
            "result": {
                "token": "6c680d5c-9494-4e60-8a96-24bef609efda",
                "ref_code": "3834222"
                    }
            }}
    return result

def mock_success_verify_otp(x, y):
    result = {
        'ok': True, 
        'result':{
            "code": "000",
            "detail": "OK.",
            "result": {
                "status": True
            }
        }
    }
    return result

def mock_fail_verify_otp(x, *args):
    result = {
        'ok': False, 
        'result':{
            "code": "1006",
            "detail": "Token is invalid.",
            "result": None
        }
    }
    return result



# Create your tests here.
class TestOTP(TestCase):
    
    def setUp(self):
        self.otp = Otp()
        self.line_id = 'test1'
        self.full_name = 'test1'
        self.mobile_no = '0223232323'
        self.otp_code = '3834222'

    @mock.patch('otp.otp_service.Otp.get_otp', side_effect=mock_get_otp)
    def test_success_get_otp(self, *args):
        is_pass, ref_code = self.otp.register_get_otp('test1', '0223232323', 'test1')
        otp = OtpRequest.objects.filter(line_id='test1', full_name=self.full_name, mobile_no=self.mobile_no).first()
        self.assertEqual(otp.full_name, 'test1')
        self.assertEqual(otp.line_id, self.line_id)
        self.assertEqual(ref_code, self.otp_code)
        self.assertTrue(is_pass)
    
    @mock.patch('otp.otp_service.Otp.get_otp', side_effect=mock_fail_verify_otp)
    def test_fail_get_otp(self, *args):
        is_pass, ref_code = self.otp.register_get_otp('test1', '0223232323', 'test1')
        otp = OtpRequest.objects.filter(line_id='test1', full_name=self.full_name, mobile_no=self.mobile_no).count()
        self.assertEqual(otp, 0)
        self.assertFalse(is_pass)
    
    @mock.patch('otp.otp_service.Otp.verify_otp', side_effect=mock_success_verify_otp)
    def test_success_verify_otp(self, *args):
        OtpRequest.objects.create(line_id=self.line_id, full_name=self.full_name, mobile_no=self.mobile_no, ref_code=self.otp_code
            ,token='123'
        )
        state ,*_ = self.otp.register_verify_otp(self.line_id, self.line_id)
        self.assertTrue(state)
    
    @mock.patch('otp.otp_service.Otp.verify_otp', side_effect=mock_success_verify_otp)
    def test_fail_verify_otp(self, *args):
        # otp count > 3
        OtpRequest.objects.create(line_id=self.line_id, full_name=self.full_name, mobile_no=self.mobile_no, ref_code=self.otp_code
            ,token='123', count=4
        )
        state ,*_ = self.otp.register_verify_otp(self.line_id, self.line_id)
        self.assertFalse(state)