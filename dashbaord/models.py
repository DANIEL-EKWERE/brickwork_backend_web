from django.db import models
from django.utils import timezone

class TaskHistory(models.Model):
    task_id = models.CharField(max_length=255, unique=True)
    script_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="PENDING")
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            self.duration = self.end_time - self.start_time
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.script_name} ({self.task_id}) - {self.status}"



class IngestionLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.created_at}] {self.message[:50]}"


class UploadedXML(models.Model):
    file = models.FileField(upload_to="data/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name