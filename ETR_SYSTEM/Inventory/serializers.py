from rest_framework import serializers
from .models import Category, Product



class CategorySerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "code"]


class ProductSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "sku",
            "description",
            "unit_price",
            "quantity",
        ]

    # def save(self, *args, **kwargs):
    #     if not self.instance.sku:
    #         self.instance.sku = f"{self.instance.category.code}-{self.instance.id}"
    #     super().save(*args, **kwargs)

    def validate_quantity(self, value):
        if value <= 20:
            raise serializers.ValidationError(
                "⚠️ Warning: The low stock threshold is set below the recommended minimum of 20."
            )
        return value
    