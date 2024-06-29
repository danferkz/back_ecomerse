from django.http import Http404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

class LatestProductsList(APIView):
    def get(self, request, format=None):
        """
        Get the list of the latest products.
        """
        products = Product.objects.all().order_by('-date_added')[:4]  # Get the 4 most recent products
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        """
        Get a product based on category and product slugs.
        """
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404("Product not found")
    
    def get(self, request, category_slug, product_slug, format=None):
        """
        Get the details of a specific product.
        """
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class CategoryDetail(APIView):
    def get_object(self, category_slug):
        """
        Get a category based on its slug.
        """
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404("Category not found")
    
    def get(self, request, category_slug, format=None):
        """
        Get the details of a specific category.
        """
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

class ProductList(ListAPIView):
    """
    List all products, or filter by category.
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned products to a given category.
        """
        category_slug = self.kwargs.get('category_slug', None)
        if category_slug:
            return Product.objects.filter(category__slug=category_slug)
        return Product.objects.all()

class CategoryList(ListAPIView):
    """
    List all categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    

class Search(APIView):
    """
    Search for products based on a query string.
    """
    def post(self, request, format=None):
        query = request.data.get('query', '')

        if query:
            products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        else:
            return Response({"products": []}, status=status.HTTP_200_OK)
