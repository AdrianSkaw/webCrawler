
from django.urls import path, include

from crawler.controller.crawler_controller import CrawlerController

urlpatterns = [
    path('api/v1/crawler', CrawlerController.as_view(), name='crawler'),
]