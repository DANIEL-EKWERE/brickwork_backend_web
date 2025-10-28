from django.contrib import admin
from .models import IngestionLog, TaskHistory,UploadedXML
# Register your models here.
admin.site.register(TaskHistory)
admin.site.register(IngestionLog)
admin.site.register(UploadedXML)
