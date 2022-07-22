from django.urls import path
from delivery.views import MyCart, NewMyCart, WebhookAPI, OrderView, OrderAPI, RestaurantView, RestaurantAllView, RestaurantDetail, MenutDetail,TestMap
from delivery.views import Enroll,LocationDetail,LocationSave,History
urlpatterns = [
    # mvc
    path('', RestaurantView.as_view()),
    path('<int:pk>/', RestaurantDetail.as_view(), name='restaurant_detail'),
    path('<int:res_pk>/<int:pk>/', MenutDetail.as_view(), name='menu_detail'),
    path('order/', OrderView.as_view()),
    path('mycart/', MyCart.as_view(), name='mycart'),
    path('enroll/', Enroll.as_view()),
    path('location_detail/', LocationDetail.as_view()),
    path('location_save/', LocationSave.as_view()),
    path('history/<int:pk>/', History.as_view()),
    # api
    path('api/order/', OrderAPI.as_view()),
    # line
    path('webhook/', WebhookAPI.as_view()),
    path('testmap/', TestMap.as_view())
]

# admin
from delivery.views_admin import AdminView, AdminViewDetail
from delivery.view_seller import HistorySeller

urlpatterns += [
    path('admin/', AdminView.as_view()),
    path('admin/<int:pk>/', AdminViewDetail.as_view()),
    path('seller/history/<int:pk>/', HistorySeller.as_view()),
]