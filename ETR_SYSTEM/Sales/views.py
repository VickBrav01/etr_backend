from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .serializers import SalesOrderSerializer
from .models import SalesOrder, SalesItem
from rest_framework.generics import ListAPIView
from .serializers import SalesItemSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class SalesItemListView(ListAPIView):
    queryset = SalesItem.objects.all()
    serializer_class = SalesItemSerializer


class SalesOrderView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SalesOrderSerializer

    # Create a new sales order
    def post(self, request: Request):
        data = self.request.data
        try:

            item_pks = data.get("item_pks", [])
            if not item_pks:
                return Response(
                    {"message": "No items selected for the order."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Remove item_pks from data before creating SalesOrder
            order_data = data.copy()
            order_data.pop("item_pks", None)

            # Create the sales order
            sales_order = SalesOrder.objects.create(**order_data)

            # Link selected items to the sales order
            for pk in item_pks:
                item = get_object_or_404(SalesItem, pk=pk)
                sales_order.items.add(item)

            sales_order.save()

            response = {
                "message": "Sales order created successfully",
                "data": SalesOrderSerializer(sales_order).data,
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        except Exception as e:
            response = {
                "message": "Sales order creation failed",
                "error": str(e),
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
