from rest_framework import serializers
from main.models import *


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    # def create(self, validated_data):
    #     author_data = validated_data.pop("author")
    #     author, _ = Author.objects.get_or_create(**author_data)
    #
    #     book = Book.objects.create(author=author, **validated_data)
    #     return book


class BookTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTag
        fields = '__all__'


class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookImage
        fields = '__all__'

# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'


# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = '__all__'


# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = '__all__'
