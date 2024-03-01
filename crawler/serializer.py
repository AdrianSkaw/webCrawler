from rest_framework import serializers
from .models import Brand, BrandDetails


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['title', 'url']


class BrandDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandDetails
        fields = ['brand', 'price', 'strike_price']

