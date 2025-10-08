from django.contrib import admin
from .models import IngestionLog, TaskHistory
# Register your models here.
admin.site.register(TaskHistory)
admin.site.register(IngestionLog)
