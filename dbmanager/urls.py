from django.urls import path
from .views import *

app_name='dbmanager'
urlpatterns = [
    path('',index,name='index'),
    path('recovery/',recovery,name='recovery')
]