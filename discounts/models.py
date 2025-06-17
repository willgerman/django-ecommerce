import uuid
from django.db import models
from django.utils import timezone

from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
class Coupon(models.Model):
    id = models.UUIDField(
            primary_key = True, 
            default = uuid.uuid4, 
            editable = False
    ) 
    code = models.CharField(max_length=6,
                            unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=
            [MinValueValidator(0), 
            MaxValueValidator(100)],
        help_text='Percentage value (0 to 100)'
    )
    is_active = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # update date_updated
        return super().save(*args, **kwargs)

    def is_valid_and_active(self):
        if self.valid_from <= timezone.now() <= self.valid_to and self.is_active:
            return True
        return False

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"