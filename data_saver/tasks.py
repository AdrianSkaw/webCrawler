from celery import shared_task
from data_saver.repository import BrandRepository, BrandDetailsRepository

@shared_task
def save_product_to_db(product):
    """
    Save product data to the database asynchronously.
    """
    if not BrandRepository.is_exist(product):
        BrandRepository.create(product)
    brand = BrandRepository.get_by_name(name=product.get("title"))
    BrandDetailsRepository.create(brand, product)