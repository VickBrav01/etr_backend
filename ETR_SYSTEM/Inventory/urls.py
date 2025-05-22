from django.urls import path
from .views import CategoryListCreateView, CategoryRetrieveUpdateDestroyView
from .views import ProductListCreateView, ProductRetrieveUpdateDestroyView


urlpatterns = [
    path("categories/", CategoryListCreateView.as_view(), name="categories"),
    path(
        "categories/<int:pk>/",
        CategoryRetrieveUpdateDestroyView.as_view(),
        name="category-detail",
    ),
    path("products/", ProductListCreateView.as_view(), name="products"),
    path(
        "products/<int:pk>/",
        ProductRetrieveUpdateDestroyView.as_view(),
        name="product-detail",
    ),
]
