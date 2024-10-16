from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_slug = models.SlugField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    category_image = models.ImageField(upload_to="photos/categories", blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category_name