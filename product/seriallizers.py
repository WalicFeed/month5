from rest_framework import serializers
from .models import Product, Category, Review

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title price category'.split()
        # # fields = '__all__'
        # exclude = 'id text'.split()

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name count'.split()
        # # fields = '__all__'
        # exclude = 'id text'.split()

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id product'.split()
        # # fields = '__all__'
        # exclude = 'id text'.split()

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProductReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewDetailSerializer(many=True)
    class Meta:
        model = Product
        fields = 'id title price reviews rating'.split()