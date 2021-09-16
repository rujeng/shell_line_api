from line.line_service import Line
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from line.models import TransactionForm,LineOfficial
from line.form.web_form import WebForm
from django.shortcuts import redirect
from django.core.exceptions import SuspiciousOperation
# Create your views here.

class WebForm(View):

    def get(self, request):
        form = WebForm()
        return render(request, template_name='form.html')
    
    def post(self, request):
        user_id = request.GET.get("user_id")
        channel_id = request.GET.get("channel_id")
        fullname = request.POST['fullname']
        mobileno = request.POST['mobileno']
        locationRadio = request.POST['locationRadio']
        date = request.POST['date']
        time = request.POST['time']
        line = Line()
        meta_dat = { 'fullname' : fullname , 'mobileno' : mobileno}
        line_official = LineOfficial.objects.filter(channel_id = channel_id).first()
        channel_access_token = line_official.channel_access_token
        print('channel_access_token ' , channel_access_token)
        line.push_message(user_id,meta_dat,channel_access_token)
        # fullname = request.POST['fullname']
        TransactionForm.objects.create(meta_data = meta_dat,line_official = line_official)
        return render(request, template_name='form.html')

        # def __businesslogic(self,meta_dat):

        # def __validate(self,meta_dat):



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
        channel_id = request.GET.get("channel_id")
        user_id,state = self.__businesslogic(code,channel_id)
        if state:
            return redirect(f'/line/form?user_id={user_id}&channel_id={channel_id}')
        
        raise SuspiciousOperation("Invalid request; see documentation for correct paramaters")

        # line = Line()
        # queries = { 'code' : code , 'channel_id' : channel_id }
        # get_token_response = line.get_token(queries)

    def __businesslogic(self,code,channel_id):
        line = Line()
        queries = { 'code' : code , 'channel_id' : channel_id }
        line_official = LineOfficial.objects.filter(channel_id = queries['channel_id']).first()
        client_id = line_official.client_id
        channel_secrete = line_official.channel_secrete
        get_token_response = line.get_token(queries,client_id,channel_secrete)
        if get_token_response['ok'] : 
            access_token = get_token_response['result']['access_token']
            get_profile_response = line.get_profile(access_token)
            if get_profile_response['ok']:
                user_id = get_profile_response['result']['userId']
                return user_id,True
        return None,False

                
        


        