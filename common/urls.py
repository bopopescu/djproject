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
    path('model_detail/',model_detail,name='model_detail'),
    path('mysqldb/',mysqldb,name='mysqldb'),
    path('upload-files/',UploadFilesView.as_view(), name='upload_files'),
    path('remove_file/<int:f_id>/',remove_file,name='remove_file'),
    path('update_files/',update_files,name='update_files'),
    path('tasks/',tasks,name='tasks'),
    path('exec_tasks/',exec_tasks,name='run_tasks')
]