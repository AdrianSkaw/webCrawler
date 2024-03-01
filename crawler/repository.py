from crawler.models import Brand, BrandDetails
from rest_framework.exceptions import NotFound


class BaseRepository:
    @staticmethod
    def create(model_cls, **kwargs):
        return model_cls.objects.create(**kwargs)

    @staticmethod
    def filter(model_cls, **kwargs):
        return model_cls.objects.filter(**kwargs)

    @staticmethod
    def get(model_cls, **kwargs):
        try:
            return model_cls.objects.get(**kwargs)
        except model_cls.DoesNotExist:
            raise NotFound(f"{model_cls.__name__} not exist")


class BrandRepository(BaseRepository):
    @staticmethod
    def create(product):
        return BaseRepository.create(
            Brand,
            title=product["title"],
            url=product["url"]
        )

    @staticmethod
    def is_exist(product):
        return BaseRepository.filter(Brand, title=product.get("title"))

    @staticmethod
    def get_by_name(name):
        return BaseRepository.get(Brand, title=name)


class BrandDetailsRepository(BaseRepository):
    @staticmethod
    def create(brand: Brand, product):
        return BaseRepository.create(
            BrandDetails,
            title=brand,
            price=product.get("price", -1),
            strike_price=-1
        )
