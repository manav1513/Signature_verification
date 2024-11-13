from django.db import models

class Signature(models.Model):
    image = models.ImageField(upload_to='signatures/')  # Directory to store uploaded signature images
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Track when the signature was uploaded

    def __str__(self):
        return f"Signature {self.id} uploaded at {self.uploaded_at}"
