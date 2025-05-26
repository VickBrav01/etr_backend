from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import SalesOrder, SalesItem

class SalesOrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.sales_item = SalesItem.objects.create(name="Test Item", price=10.00)

    def test_create_sales_order(self):
        response = self.client.post('/sales/orders/', {
            'items': [
                {'sku': self.sales_item.pk, 'quantity': 2}
            ]
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SalesOrder.objects.count(), 1)
        self.assertEqual(SalesOrder.objects.get().items.count(), 1)

    def test_create_sales_order_with_invalid_item(self):
        response = self.client.post('/sales/orders/', {
            'items': [
                {'sku': 999, 'quantity': 2}  # Invalid SKU
            ]
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_sales_order_without_items(self):
        response = self.client.post('/sales/orders/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)