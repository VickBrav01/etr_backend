from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.shortcuts import get_object_or_404


# Create Category
# Update Category
# Delete Category
class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs):
        category = self.request.data
        serializer = self.serializer_class(data=category)

        try:
            if serializer.is_valid():
                serializer.save()
                response = {
                    "message": "Category Created",
                    "data": serializer.data,
                }
                return Response(data=response, status=status.HTTP_201_CREATED)
            else:
                raise ValueError(serializer.errors)

        except Exception as e:
            response = {
                "message": "Category Creation Failed",
                "error": str(e),
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


# Create product
# Get product
# Update product
# Delete product
class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs):
        product = self.request.data
        serializer = self.serializer_class(data=product)

        try:
            if serializer.is_valid():
                serializer.save()
                response = {
                    "message": "Product Created",
                    "data": serializer.data,
                }
                return Response(data=response, status=status.HTTP_201_CREATED)
            else:
                raise ValueError(serializer.errors)

        except Exception as e:
            response = {
                "message": "Product Creation Failed",
                "error": str(e),
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# class ProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [IsAuthenticated]

# def get(self, request: Request, *args, **kwargs):
#     product = self.get_object()
#     serializer = self.serializer_class(product)
#     return Response(serializer.data, status=status.HTTP_200_OK)


class ProductRetrieveUpdateDestroyView(APIView):
    # model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request: Request, *args, **kwargs):
        data = self.request.data
        pk = self.kwargs.get("pk")
        product = get_object_or_404(Product, pk=pk)
        # product = self.model.objects.filter(id=pk)
        if not product:
            return Response(
                {"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(instance=product, data=data)

        try:
            if serializer.is_valid():
                serializer.save()
                response = {
                    "message": "Product Updated",
                    "data": serializer.data,
                }
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                raise ValueError(serializer.errors)

        except Exception as e:
            response = {
                "message": "Product Update Failed",
                "error": str(e),
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        if not pk:
            return Response(
                {"message": "Product ID not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # product = self.model.objects.filter(pk=pk)
        product = get_object_or_404(Product, pk=pk)

        serializer = self.serializer_class(product)
        response = {
            "message": "Product Retrieved",
            "data": serializer.data,
        }
        return Response(data=response, status=status.HTTP_200_OK)

    def destroy(self, request: Request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        if not pk:
            return Response(
                {"message": "Product ID not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # product = self.model.objects.filter(pk=pk)
        product = get_object_or_404(Product, pk=pk)

        if not product:
            return Response(
                {"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )
        product.delete()
        response = {
            "message": "Product Deleted",
        }
        return Response(data=response, status=status.HTTP_204_NO_CONTENT)
