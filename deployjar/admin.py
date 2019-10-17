from django.contrib import admin
from .models import *
# Register your models here.
class HostAdmin(admin.ModelAdmin):
    list_display = ('name','ip','version','config','position','created_at')
class HostUserAdmin(admin.ModelAdmin):
    list_display = ('name','password','created_at')
class JarappAdmin(admin.ModelAdmin):
    list_display = ('name','port','jar_dir','created_at')
class ScriptsAdmin(admin.ModelAdmin):
    list_display = ('name','script_dir')

admin.site.register(Host,HostAdmin)
admin.site.register(HostUser,HostUserAdmin)
admin.site.register(Jarapp,JarappAdmin)
admin.site.register(Script,ScriptsAdmin)
admin.site.register(Instance)
admin.site.register(JarModel)
admin.site.register(Domain)