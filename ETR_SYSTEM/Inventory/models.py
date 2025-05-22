from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.name[:4].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}: ({self.code})"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    sku = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=16.00)
    low_stock_threshold = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"{self.category.code}-{self.id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
