from django.urls import path
from .views import *
app_name = 'deployjar'
urlpatterns = [
    path('deploy/',deploy,name='deploy'),
    path('exec_deployment/',exec_deployment,name='exec_deployment'),
    path('control/',control,name='control')
]