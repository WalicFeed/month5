from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category, Review
from django.forms import model_to_dict
from . import seriallizers
from rest_framework import status

@api_view(http_method_names=['GET'])
def product_list_api_view(request):
    products = Product.objects.all()
    data = seriallizers.ProductListSerializer(products, many=True).data
    return Response(
        data=data
    )

@api_view(http_method_names=['GET'])
def product_detail_api_fiew(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not found!'}, status=status.HTTP_404_NOT_FOUND)
    data = seriallizers.ProductDetailSerializer(product, many=False).data
    return Response(data=data)

@api_view(http_method_names=['GET'])
def category_list_api_view(request):
    categories = Category.objects.all()
    data = seriallizers.CategoryListSerializer(categories, many=True).data
    return Response(
        data=data
    )

@api_view(http_method_names=['GET'])
def category_detail_api_fiew(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'Category not found!'}, status=status.HTTP_404_NOT_FOUND)
    data = seriallizers.CategoryDetailSerializer(category, many=False).data
    return Response(data=data)

@api_view(http_method_names=['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    data = seriallizers.ReviewListSerializer(reviews, many=True).data
    return Response(
        data=data
    )

@api_view(http_method_names=['GET'])
def review_detail_api_fiew(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found!'}, status=status.HTTP_404_NOT_FOUND)
    data = seriallizers.ReviewDetailSerializer(review, many=False).data
    return Response(data=data)

@api_view(http_method_names=['GET'])
def products_reviews_api_view(request):
    products = Product.objects.prefetch_related('reviews').all()
    data = seriallizers.ProductReviewsSerializer(products, many=True).data
    return Response(data=data)