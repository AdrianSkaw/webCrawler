
from django.urls import path

from crawler.views import CrawlerController

urlpatterns = [
    path('api/v1/crawler', CrawlerController.as_view(), name='crawler'),
]