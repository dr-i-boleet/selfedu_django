from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='main'),
    path('rooms/<slug:room_slug>/', RoomView.as_view(), name='room'),
    path('about/', about, name='about'),
    path('feedback/', feedback, name='feedback'),
    path('add_plc/', AddPlc.as_view(), name='add_plc'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('plc/<slug:plc_slug>/', PlcView.as_view(), name='plc'),
    path('api/v1/plclist/', PlcApiView.as_view()),
    path('test/api/v1/plclist/', PlcGenApiView.as_view()),
    path('test/api/v1/plc_post/', PlcGenApiView.as_view()),
    path('test/api/v1/plc/<int:pk>/', PlcGenApiView.as_view())
]
