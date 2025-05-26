from rest_framework import serializers
from .models import SalesOrder, SalesItem


class SalesItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesItem
        fields = "__all__"


class SalesOrderSerializer(serializers.ModelSerializer):
    items = SalesItemSerializer(many=True)

    class Meta:
        model = SalesOrder
        fields = "__all__"

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        sales_order = SalesOrder.objects.create(**validated_data)
        for item_data in items_data:
            SalesItem.objects.create(order=sales_order, **item_data)
        return sales_order

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)
        instance = super().update(instance, validated_data)
        if items_data:
            instance.items.all().delete()  # Clear existing items
            for item_data in items_data:
                SalesItem.objects.create(order=instance, **item_data)
        return instance
