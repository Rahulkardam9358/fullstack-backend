from rest_framework import serializers
from product.models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['user']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    class Meta:
        model = Product
        exclude = ['user']



class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.fullName', read_only=True)
    class Meta:
        model = Review
        fields = ['content', 'rate', 'user','product']