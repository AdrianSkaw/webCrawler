from crawler.models import Brand, BrandDetails
from rest_framework.exceptions import NotFound

from crawler.serializer import BrandSerializer, BrandDetailsSerializer


class BrandRepository:
    @staticmethod
    def create(product_data):
        serializer = BrandSerializer(data=product_data)
        if serializer.is_valid():
            return serializer.save()
        else:
            # Obsługa błędów walidacji
            pass

    # @staticmethod
    # def is_exist(product_data):
    #     try:
    #         Brand.objects.get(title=product_data.get("title"))
    #         return True
    #     except Brand.DoesNotExist:
    #         return False

    @staticmethod
    def is_exist(product):
        obj = Brand.objects.filter(title=product.get("title"))
        return obj

    @staticmethod
    def get_by_name(name):
        try:
            return Brand.objects.get(title=name)
        except Brand.DoesNotExist:
            raise NotFound("Brand not exist")


class BrandDetailsRepository:
    @staticmethod
    def create(brand, product_data):
        product_data['brand'] = brand.id
        serializer = BrandDetailsSerializer(data=product_data)
        if serializer.is_valid():
            return serializer.save()
        else:
            # Obsługa błędów walidacji
            pass
# from crawler.models import Brand, BrandDetails
# from rest_framework.exceptions import NotFound
#
#
# class BrandRepository:
#     @staticmethod
#     def create(product):
#         price = product.get('price')
#         brand = Brand.objects.create(
#             title=product["title"],
#             url=product["url"]
#         )
#         return brand
#
#     @staticmethod
#     def is_exist(product):
#         return Brand.objects.filter(title=product.get("title"))
#
#     @staticmethod
#     def get_by_name(name):
#         try:
#             brand = Brand.objects.get(title=name)
#         except Brand.DoesNotExist:
#             raise NotFound("Brand not exist")
#         return brand
#
#
# class BrandDetailsRepository:
#     @staticmethod
#     def create(brand: Brand, product):
#         brand_price = BrandDetails.objects.create(
#             title=brand,
#             price=product.get("price", -1),
#             strike_price=-1
#         )
