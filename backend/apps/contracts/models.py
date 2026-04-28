from django.conf import settings
from django.db import models


class Contract(models.Model):
    class Status(models.TextChoices):
        UPLOADED = "uploaded", "Uploaded"
        PROCESSING = "processing", "Processing"
        ANALYZED = "analyzed", "Analyzed"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contracts"
    )
    document = models.ForeignKey(
        "files.Document", on_delete=models.CASCADE, related_name="contracts"
    )
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.UPLOADED
    )
    raw_text = models.TextField()
    file_extension = models.CharField(max_length=10)
    lang = models.CharField(max_length=10, default="en")
    signed_at = models.DateTimeField(null=True, blank=True)
    risk_score = models.FloatField(default=0)
    summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
