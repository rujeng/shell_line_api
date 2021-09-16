from line.line_service import Line
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from line.models import TransactionForm
from line.form.web_form import WebForm
# Create your views here.

class WebForm(View):

    def get(self, request):
        form = WebForm()
        return render(request, template_name='form.html')
    
    def post(self, request):
        fullname = request.POST['fullname']
        fullname = request.POST['fullname']
        fullname = request.POST['fullname']
        fullname = request.POST['fullname']
        # TransactionForm.objects.create()
        return render(request, template_name='form.html')


class TestView(View):

    def get(self, request):
        line = Line()
        data = {
            'message': 'test'
        }
        r = line.notify(data, 'oxCyrrgf1jWuQFU7c6yBghkJDmmRhmvvDNN6xTHlb5i')
        return JsonResponse(r)