from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category, Review
from . import seriallizers
from rest_framework import status
from django.db import transaction

@api_view(http_method_names=['GET', 'POST'])
def product_list_create_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = seriallizers.ProductListSerializer(products, many=True).data
        return Response(
            data=data
        )
    elif request.method == 'POST':
        serializer = seriallizers.ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data.get('title')
        price = serializer.validated_data.get('price')
        description = serializer.validated_data.get('description')
        category_id = serializer.validated_data.get('category_id')
        with transaction.atomic():
            product = Product.objects.create(
                title=title,
                price=price,
                description=description,
                category_id=category_id
            )
            product.save()
        return Response(status=status.HTTP_201_CREATED, data=seriallizers.ProductDetailSerializer(product).data)

@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def product_detail_api_fiew(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not found!'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = seriallizers.ProductDetailSerializer(product, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = seriallizers.ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            product.title = serializer.validated_data.get('title')
            product.price = serializer.validated_data.get('price')
            product.description = serializer.validated_data.get('description')
            product.category_id = serializer.validated_data.get('category_id')
            product.save()
        return Response(status=status.HTTP_200_OK, data=seriallizers.ProductDetailSerializer(product).data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=['GET', 'POST'])
def category_list_create_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        data = seriallizers.CategoryListSerializer(categories, many=True).data
        return Response(
            data=data
        )
    elif request.method == 'POST':
        serializer = seriallizers.CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            category = Category.objects.create(name=serializer.validated_data.get('name'))
        return Response(status=status.HTTP_201_CREATED, data=seriallizers.CategoryDetailSerializer(category).data)

@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def category_detail_api_fiew(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'Category not found!'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = seriallizers.CategoryDetailSerializer(category, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = seriallizers.CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            category.name = serializer.validated_data.get('name')
            category.save()
        return Response(status=status.HTTP_200_OK, data=seriallizers.CategoryDetailSerializer(category).data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=['GET', 'POST'])
def review_list_create_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = seriallizers.ReviewListSerializer(reviews, many=True).data
        return Response(
            data=data
        )
    elif request.method == 'POST':
        serializer = seriallizers.ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            review = Review.objects.create(
                text=serializer.validated_data.get('text'),
                product_id=serializer.validated_data.get('product_id'),
                stars=serializer.validated_data.get('stars')
            )
        return Response(status=status.HTTP_201_CREATED, data=seriallizers.ReviewDetailSerializer(review).data)

@api_view(http_method_names=['GET', 'PUT', 'DELETE'])
def review_detail_api_fiew(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found!'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = seriallizers.ReviewDetailSerializer(review, many=False).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = seriallizers.ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            review.text = serializer.validated_data.get('text')
            review.product_id = serializer.validated_data.get('product_id')
            review.stars = serializer.validated_data.get('stars')
            review.save()
        return Response(status=status.HTTP_200_OK, data=seriallizers.ReviewDetailSerializer(review).data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=['GET'])
def products_reviews_api_view(request):
    products = Product.objects.prefetch_related('reviews').all()
    data = seriallizers.ProductReviewsSerializer(products, many=True).data
    return Response(data=data)