from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'),
    path('<int:app_id>/deploy/',deploy,name='deploy'),
    path('exec_deployment/',exec_deployment,name='exec_deployment'),
    path('control/',control,name='control')
]