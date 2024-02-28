from crawler.model.models import Brand, BrandDetails
from rest_framework.exceptions import NotFound


class BrandRepository:
    @staticmethod
    def create(product):
        price = product.get('price')
        brand = Brand.objects.create(
            title=product["title"],
            url=product["url"]
        )
        return brand

    @staticmethod
    def is_exist(product):
        return Brand.objects.filter(title=product.get("title"))

    @staticmethod
    def get_by_name(name):
        try:
            brand = Brand.objects.get(title=name)
        except Brand.DoesNotExist:
            raise NotFound("Brand not exist")
        return brand


class BrandDetailsRepository:
    @staticmethod
    def create(brand: Brand, product):
        brand_price = BrandDetails.objects.create(
            title=brand,
            price=product.get("price", -1),
            strike_price=-1
        )
