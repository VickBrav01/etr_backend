from rest_framework import serializers
from .models import SalesItem, SalesOrder
from Inventory.models import Product
from django.db import transaction



class SalesItemSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(write_only=True)

    class Meta:
        model = SalesItem
        fields = ['sku', 'quantity', 'price']
        extra_kwargs = {
            'price': {'read_only': True}
        }

    def validate(self, data):
        sku = data.get('sku')
        quantity = data.get('quantity')

        try:
            product = Product.objects.get(sku=sku)
        except Product.DoesNotExist:
            raise serializers.ValidationError(f"Product with SKU '{sku}' does not exist.")

        if product.quantity < quantity:
            raise serializers.ValidationError(f"Not enough stock for product '{product.name}' (Available: {product.quantity}, Requested: {quantity})")

        data['product'] = product
        data['price'] = product.price
        return data
    
    
class SalesOrderSerializer(serializers.ModelSerializer):
    items = SalesItemSerializer(many=True)

    class Meta:
        model = SalesOrder
        fields = ['id', 'items', 'total_price', 'order_date', 'customer_name', 'customer_number']
        read_only_fields = ['id', 'total_price', 'order_date']

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        sales_order = SalesOrder.objects.create(**validated_data)

        total = 0

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            price = item_data['price']

            # Deduct stock
            product.quantity -= quantity
            product.save()

            # Create SalesItem
            SalesItem.objects.create(
                sales_order=sales_order,
                product=product,
                quantity=quantity,
                price=price
            )

            # Add to total price
            total += quantity * price

        sales_order.total_price = total
        sales_order.save()

        return sales_order
    