from django.db import models

class SalesItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class SalesOrder(models.Model):
    items = models.ManyToManyField(SalesItem)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        total = sum(item.price * item.quantity for item in self.items.all())
        self.total_amount = total
        self.save()

    def __str__(self):
        return f"Sales Order #{self.id} - Total: {self.total_amount}"