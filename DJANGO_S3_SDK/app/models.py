from django.db import models

class Picture(models.Model):
    img = models.ImageField(upload_to="static/", blank=True)