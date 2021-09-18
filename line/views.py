from line.line_service import Line
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from line.models import TransactionForm,LineLogin,LineMessage
from line.form.web_form import WebForm
from django.shortcuts import redirect
from django.core.exceptions import SuspiciousOperation
# Create your views here.

class WebForm(View):

    def get(self, request):
        form = WebForm()
        return render(request, template_name='form.html')
    
    def post(self, request):
        user_id = request.GET.get("user_id", None)
        branch_id = request.GET.get("branch_id", None)
        fullname = request.POST.get('fullname', None)
        mobileno = request.POST.get('mobileno', None)
        locationRadio = request.POST.get('locationRadio', None)
        date = request.POST.get('date', None)
        time = request.POST.get('time', None)
        meta_dat = { 'fullname' : fullname , 'mobileno' : mobileno}
        if self.__businesslogic(meta_dat,branch_id,user_id):
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'}, status=400)


    def __businesslogic(self,meta_dat,branch_id,user_id):        
        line = Line()
        line_message = LineMessage.objects.filter(branch_id = branch_id).first()
        channel_access_token = line_message.channel_access_token
        res = line.push_message(user_id,meta_dat,channel_access_token)
        if res['ok']:
            line.notify(meta_dat,channel_access_token)
            TransactionForm.objects.create(meta_data = meta_dat,line_message = line_message,user_id = user_id)
            return True
        return False
        

class TestView(View):

    def get(self, request):
        line = Line()
        data = {
            'message': 'test'
        }
        meta_dat = { 'fullname' : '' , 'mobileno' : ''}
        r = line.push_message('Ue747b02b8d096f682e596cb4d4dfddaf',meta_dat=meta_dat)
        # r = line.notify(data, 'oxCyrrgf1jWuQFU7c6yBghkJDmmRhmvvDNN6xTHlb5i')
        return JsonResponse(r)
        
        
class LineHookView(View):

    def get(self, request):
        code = request.GET.get("code")
        branch_id = request.GET.get("branch_id")
        user_id,state = self.__businesslogic(code,branch_id)
        if state:
            return redirect(f'/line/form?user_id={user_id}&branch_id={branch_id}')
        
        raise SuspiciousOperation("Invalid request; see documentation for correct paramaters")

        # line = Line()
        # queries = { 'code' : code , 'channel_id' : channel_id }
        # get_token_response = line.get_token(queries)

    def __businesslogic(self,code,branch_id):
        line = Line()
        line_login = LineLogin.objects.filter(branch_id = branch_id).first()
        channel_id = line_login.channel_id
        channel_secret = line_login.channel_secret
        get_token_response = line.get_token(code,branch_id,channel_id,channel_secret)
        print('get to ' , get_token_response)
        if get_token_response['ok'] : 
            access_token = get_token_response['result']['access_token']
            get_profile_response = line.get_profile(access_token)
            if get_profile_response['ok']:
                user_id = get_profile_response['result']['userId']
                return user_id,True
        return None,False

                
        


        