from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='main'),
    path('rooms/<int:roomid>/', rooms),
    path('about/', about, name='about'),
    path('feedback/', feedback, name='feedback'),
    path('add_plc/', add_plc, name='add_plc'),
    path('login/', login, name='login'),
    path('plc/<int:plc_id>/', plc, name='plc')
]
