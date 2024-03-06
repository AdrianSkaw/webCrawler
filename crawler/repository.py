# from crawler.models import Brand
# from rest_framework.exceptions import NotFound
# from rest_framework import serializers
# from crawler.serializer import BrandSerializer, BrandDetailsSerializer
#
#
# class BaseRepository:
#
#     @staticmethod
#     def filter(model_cls, **kwargs):
#         return model_cls.objects.filter(**kwargs)
#
#     @staticmethod
#     def get(model_cls, **kwargs):
#         try:
#             return model_cls.objects.get(**kwargs)
#         except model_cls.DoesNotExist:
#             raise NotFound(f"{model_cls.__name__} not exist")
#
#
# class BrandRepository(BaseRepository):
#     @staticmethod
#     def create(product_data):
#         serializer = BrandSerializer(data=product_data)
#         if serializer.is_valid():
#             return serializer.save()
#         else:
#             raise serializers.ValidationError("Failed to create Brand object")
#
#     @staticmethod
#     def is_exist(product):
#         return BaseRepository.filter(Brand, title=product.get("title"))
#
#     @staticmethod
#     def get_by_name(name):
#         return BaseRepository.get(Brand, title=name)
#
#
# class BrandDetailsRepository(BaseRepository):
#     @staticmethod
#     def create(brand, product_data):
#         product_data['brand'] = brand.id
#         serializer = BrandDetailsSerializer(data=product_data)
#         if serializer.is_valid():
#             return serializer.save()
#         else:
#             raise serializers.ValidationError("Failed to create BrandDetails object")
