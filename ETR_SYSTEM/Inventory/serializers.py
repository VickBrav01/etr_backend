from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "code"]
        read_only_fields = ["id", "code"]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

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
        read_only_fields = ["id", "sku"]

    def validate_quantity(self, value):
        if value <= 20:
            raise serializers.ValidationError(
                "⚠️ Warning: The low stock threshold is set below the recommended minimum of 20."
            )
        return value
