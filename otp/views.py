from django.shortcuts import render, redirect
from django.views.generic import View
from otp.otp_service import Otp
from line.models import CustomUser
# Create your views here.

class OTPVerify(View):

    def get(self, request):
        line_id = request.GET.get("user_id", None)
        branch_id = request.GET.get("branch_id", None)
        full_name = request.GET.get('full_name', None)
        mobileno = request.GET.get('mobileno', None)
        action = request.GET.get('action',None)
        otp = Otp()
        state,ref_code = otp.register_get_otp(line_id,mobileno,full_name)
        if state:
            context = {'ref_code': ref_code, 'line_id': line_id, 'branch_id': branch_id, 
            'action': action, 'full_name': full_name, 'mobileno': mobileno}
            return render(request, 'otp.html', context=context)
        return render(request, 'error.html')

    def post(self, request):
        line_id = request.POST.get('user_id',None)
        ref_code = request.POST.get('ref_code', None)
        branch_id = request.POST.get('branch_id', None)
        otp_code = request.POST.get('otp_code',None)
        action = request.POST.get('action',None)
        full_name = request.POST.get('full_name',None)
        mobileno = request.POST.get('mobileno',None)
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
            
            if action == 'form':
                return redirect(f'/line/car/?user_id={line_id}&branch_id={branch_id}')
            elif action == 'history':
                return redirect(f'/line/history/?user_id={line_id}&branch_id={branch_id}&page=1&car_id=')
            elif action == 'calculate':
                return redirect(f'/item/price/?user_id={line_id}&branch_id={branch_id}&car_id=')
            else:
                return render(request, 'error.html')
        else:
           context = {'ref_code': ref_code, 'line_id': line_id, 'branch_id': branch_id, 'action': action, 
           'full_name': full_name, 'mobileno': mobileno, 'error_message':error_message}
           return render(request, 'otp.html', context=context)

    def check_old_user_and_update_line_id(self, meta_data):
        '''
            ???????????? ??????????????????????????????????????? ???????????????????????? user ????????? update full_name, 
            line_id ??????????????????????????????????????????????????????
        '''
        mobile = meta_data['mobile']
        full_name = meta_data['full_name']
        line_id = meta_data['line_id']
        user, is_existed = CustomUser.objects.get_or_create(mobile_no=mobile)
        user.full_name = full_name
        user.line_id = line_id
        user.save()
        return
