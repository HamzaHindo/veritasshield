from django.conf import settings
from django.db import models


class Document(models.Model):
    file = models.FileField(upload_to="contracts/")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_extension = models.CharField(max_length=10)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    signed_at = models.DateTimeField(null=True, blank=True)
    lang = models.CharField(max_length=10, default="en")
    raw_text = models.TextField(blank=True, null=True)
    confidence = models.FloatField(default=0.0)
    title = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.file.name
