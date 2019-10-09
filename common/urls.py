from django.urls import path
from .views import *

app_name = 'common'
urlpatterns = [
    path('checkbackup/',checkbackup,name='checkbackup'),
    path('execcheck/',execcheck,name='execcheck')
]