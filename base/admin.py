from django.contrib import admin
from base.models import *
# Register your models here.
admin.site.register(Projects),
admin.site.register(ProjectMembers),
admin.site.register(Tasks),
admin.site.register(Comments)