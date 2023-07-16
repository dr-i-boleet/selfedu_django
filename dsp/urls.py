from django.template.defaulttags import url
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter, DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'room', RoomViewSet, 'room')

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
    path('test/api/v1/plc/<int:pk>/', PlcGenApiView.as_view()),
    path('test/api/v1/', include(router.urls)),
    path('test/api/v1/room_per/list/', RoomListCreateApiView.as_view()),
    path('test/api/v1/room_per/<int:pk>/', RoomUpdateApiView.as_view()),
    path('test/api/v1/room_perd/<int:pk>/', RoomDestroyApiView.as_view()),
    path('test/api/v1/auth/', include('rest_framework.urls')),
    path('djoser/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
