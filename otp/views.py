from django.shortcuts import render, redirect
from django.views.generic import View
# from django.shortcuts import redirect
from otp.otp_service import Otp
from line.models import CustomUser
# Create your views here.


class OTPVerify(View):

    def post(self, request):
        line_id = request.POST.get('line_id',None)
        ref_code = request.POST.get('ref_code', None)
        branch_id = request.POST.get('branch_id', None)
        otp_code = request.POST.get('otp_code',None)
        print('----------')
        # verify otp
        otp = Otp()
        state,error_message, otp_request = otp.register_verify_otp(line_id,otp_code)
        if state:
            meta_data = {
                'mobile': otp_request.mobile_no,
                'full_name': otp_request.full_name,
                'line_id': line_id
            }
            self.check_old_user_and_update_line_id(meta_data)
            return redirect(f'/line/car/?user_id={line_id}&branch_id={branch_id}')
        context = {'ref_code': ref_code, 'line_id': line_id, 'branch_id': branch_id,'error_message':error_message}
        return render(request, 'otp.html', context=context)

    def check_old_user_and_update_line_id(self, meta_data):
        '''
            เช็ค เบอร์โทรศัพท์ ว่าเคยมี user ไหม update full_name, 
            line_id ไม่ว่าอย่างไรก็ตาม
        '''
        mobile = meta_data['mobile']
        full_name = meta_data['full_name']
        line_id = meta_data['line_id']
        user, is_existed = CustomUser.objects.get_or_create(mobile_no=mobile)
        user.full_name = full_name
        user.line_id = line_id
        user.save()
        return
