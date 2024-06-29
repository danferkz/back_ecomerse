from django.urls import path

from product import views

urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view(), name='latest-products'),
    path('products/search/', views.Search.as_view(), name='search'),  # Cambiado a Search.as_view() para usar la clase APIView
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view(), name='product-detail'),
    path('products/<slug:category_slug>/', views.ProductList.as_view(), name='product-list-by-category'),  # Cambiado para listar productos por categoría
    path('categories/<slug:category_slug>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('categories/', views.CategoryList.as_view(), name='category-list'),
]
