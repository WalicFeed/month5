from rest_framework.response import Response
from .models import Product, Category, Review
from . import seriallizers
from rest_framework import status
from django.db import transaction
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return seriallizers.ProductListSerializer
        return seriallizers.ProductValidateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
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
                category_id=category_id,
            )
        return Response(
            status=status.HTTP_201_CREATED,
            data=seriallizers.ProductDetailSerializer(product).data,
        )

class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return seriallizers.ProductDetailSerializer
        return seriallizers.ProductValidateSerializer
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            instance.title = serializer.validated_data.get('title')
            instance.price = serializer.validated_data.get('price')
            instance.description = serializer.validated_data.get('description')
            instance.category_id = serializer.validated_data.get('category_id')
            instance.save()
        return Response(
            status=status.HTTP_200_OK,
            data=seriallizers.ProductDetailSerializer(instance).data,
        )

class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return seriallizers.CategoryListSerializer
        return seriallizers.CategoryValidateSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            category = Category.objects.create(name=serializer.validated_data.get('name'))
        return Response(
            status=status.HTTP_201_CREATED,
            data=seriallizers.CategoryDetailSerializer(category).data,
        )

class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    lookup_field = 'id'
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return seriallizers.CategoryDetailSerializer
        return seriallizers.CategoryValidateSerializer
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            instance.name = serializer.validated_data.get('name')
            instance.save()
        return Response(
            status=status.HTTP_200_OK,
            data=seriallizers.CategoryDetailSerializer(instance).data,
        )

class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return seriallizers.ReviewListSerializer
        return seriallizers.ReviewValidateSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            review = Review.objects.create(
                text=serializer.validated_data.get('text'),
                product_id=serializer.validated_data.get('product_id'),
                stars=serializer.validated_data.get('stars'),
            )
        return Response(
            status=status.HTTP_201_CREATED,
            data=seriallizers.ReviewDetailSerializer(review).data,
        )

class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    lookup_field = 'id'
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return seriallizers.ReviewDetailSerializer
        return seriallizers.ReviewValidateSerializer
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            instance.text = serializer.validated_data.get('text')
            instance.product_id = serializer.validated_data.get('product_id')
            instance.stars = serializer.validated_data.get('stars')
            instance.save()
        return Response(
            status=status.HTTP_200_OK,
            data=seriallizers.ReviewDetailSerializer(instance).data,
        )

class ProductsReviewsAPIView(ListAPIView):
    queryset = Product.objects.prefetch_related('reviews').all()
    serializer_class = seriallizers.ProductReviewsSerializer