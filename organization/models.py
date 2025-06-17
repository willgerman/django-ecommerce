import uuid
from django.db import models
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    id = models.UUIDField(
                primary_key = True, 
                default = uuid.uuid4, 
                editable = False) 
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True)
    thumbnail = models.ImageField(upload_to="categories/", blank=True, null=True)
    short_description = models.TextField(max_length=120, blank=True, null=True)
    description = models.TextField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        # date_updated does not change correctly

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"