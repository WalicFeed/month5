from rest_framework import serializers
from .models import Product, Category, Review
from rest_framework.exceptions import ValidationError

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

class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3)
    price = serializers.IntegerField(min_value=1)
    description = serializers.CharField(required=False)
    category_id = serializers.IntegerField()

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError(f"Category does not exist.")
        return category_id
    
class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=3)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError(f"Product does not exist.")
        return product_id
    
class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=255)