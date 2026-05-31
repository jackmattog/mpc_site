from django.db import models

class Suggestion(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.CharField(max_length=100, help_text="Phone number or WhatsApp")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.created_at.strftime('%Y-%m-%d')}"