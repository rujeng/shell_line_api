"""shellManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from line.views import ChangeCustomerNameAPIView, LineHistory, WebFormView, LineHookView, MyCar, MyHistory, CreateCarAPIView, ListItem, CarSeries
from line.views import Testview, PrivacyPolicy

urlpatterns = [
    path('form/', WebFormView.as_view()),
    path('car/', MyCar.as_view()),
    path('addcar/', CreateCarAPIView.as_view()),
    path('changename/', ChangeCustomerNameAPIView.as_view()),
    path('webhook/', LineHookView.as_view()),
    path('webhistory/', LineHistory.as_view()),
    path('history/', MyHistory.as_view()),
    path('test/', Testview.as_view(), name='test'),
    path('car-series/', CarSeries.as_view(), name='test'),
    path('itemlist/',ListItem.as_view()),
    path('test/', Testview.as_view()),
    path('privacypolicy/', PrivacyPolicy.as_view())
]
handler400 = "line.views.response_error_handler"
handler500 = 'line.views.response_error_handler'
handler404 = "line.views.response_error_handler"