from django.db import models
from django.conf import settings


# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store = models.ForeignKey('ceos.Store', on_delete=models.CASCADE)
    review_image = models.ImageField(blank=True, upload_to="store/%Y/%m/%d")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)