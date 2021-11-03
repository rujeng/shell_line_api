from django.urls import path
from delivery.views import WebhookAPI, OrderView, OrderAPI, RestaurantView, RestaurantDetail, MenutDetail

urlpatterns = [
    # mvc
    path('', RestaurantView.as_view()),
    path('<int:pk>/', RestaurantDetail.as_view(), name='restaurant_detail'),
    path('<int:res_pk>/<int:pk>/', MenutDetail.as_view(), name='menu_detail'),
    path('order/', OrderView.as_view()),
    # api
    path('api/order/', OrderAPI.as_view()),
    # line
    path('webhook/', WebhookAPI.as_view()),
]