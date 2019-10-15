from django.urls import path
from .views import *

app_name = 'common'
urlpatterns = [
    path('checkbackup/',checkbackup,name='checkbackup'),
    path('execcheck/',execcheck,name='execcheck'),
    path('host/',host,name='host'),
    path('instance/',instance,name='instance'),
    path('domain/',domain,name='domain'),
    path('model/',model,name='model'),
    path('project/',project,name='project'),
    path('<int:p_id>/deploy/',project_detail,name='project_detail'),
]