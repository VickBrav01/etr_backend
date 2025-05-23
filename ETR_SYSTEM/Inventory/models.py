from django.db import models

CHOICES = (
    ("Farm", "Farm"),
    ("Manufacturing", "Manufacturing"),
    ("Distribution", "Distribution"),
    ("E-commerce", "E-commerce"),
    ("Food Service", "Food Service"),
)


class Category(models.Model):
    name = models.CharField(max_length=100, choices=CHOICES, null=False)
    code = models.CharField(max_length=5, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.name[:4].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}: ({self.code})"


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category"
    )
    name = models.CharField(max_length=100, null=False)
    sku = models.CharField(
        max_length=100,
    )
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.pk:  # Object hasn't been saved yet
            super().save(*args, **kwargs)  # Save to generate self.id

        if not self.sku:
            self.sku = f"{self.category.code}{str(self.id).zfill(4)}"
            super().save(update_fields=["sku"])

    def __str__(self):
        return self.name
