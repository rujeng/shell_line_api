from django.urls import path
from delivery.views import WebhookAPI, OrderView, OrderAPI, RestaurantView

urlpatterns = [
    # mvc
    path('', RestaurantView.as_view()),
    path('order/', OrderView.as_view()),
    # api
    path('api/order/', OrderAPI.as_view()),
    # line
    path('webhook/', WebhookAPI.as_view()),
]