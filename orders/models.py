import uuid

from django.conf import settings
from django.db import models

class Order(models.Model):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False
    )
    invoice_id = models.CharField(
        max_length=120, 
        blank=True, 
        null=True
    )
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    email = models.EmailField()
    name = models.CharField(max_length=120, blank=True, null=True)
    phone = models.CharField(max_length=120, blank=True, null=True)
    subtotal = models.DecimalField(
        default=0.00,
        max_digits=100,
        decimal_places=2
    )
    tax = models.DecimalField(
        default=0.0,
        max_digits=100,
        decimal_places=2
    )
    shipping_fee = models.DecimalField(
        defualt=5.00,
        max_digits=100,
        decimal_places=2
    )
    total = models.DecimalField(
        default=0.0,
        max_digits=100,
        decimal_places=2
    )
    date_created = models.DateTimeField(auto_now_add=True)
    # invoice_file_field

    def get_humanize_date(self) -> str:
        pass

    def get_order_items(self):
        order_items = OrderItem.objects.filter(order=self)
        return order_items

    def __str__(self):
        if self.invoice_id is None:
            return self.name
        
        return self.invoice_id


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )
    product_uuid = models.UUIDField(
        primary_key = False,
        default = uuid.uuid4,
        editable = True
    )
    name = models.CharField(max_length=255)
    slug = models.CharField(
        max_length=255, 
        blank=True, 
        null=True
    )
    image = models.CharField(max_length=520)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(
        default=0.00,
        max_digits=100,
        decimal_places=2
    )
    line_total = models.DecimalField(
        default=0.00,
        max_digits=100,
        decimal_places=2
    )

    def __str__(self):
        return self.name

    