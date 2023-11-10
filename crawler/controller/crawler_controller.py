from dependency_injector.wiring import Provide
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from crawler.di.base_container import BaseContainer
from crawler.service.crawler_service import CrawlerService
from crawler.service.dto.request_data import RequestData
from crawler.validator.request_validator import RequestValidator


class CrawlerController(APIView):

    def __init__(self, crawler_service: CrawlerService = Provide[BaseContainer.crawler_service],
                 request_validator: RequestValidator = Provide[BaseContainer.request_validator]
                 ):
        super().__init__()
        self.__crawler_service = crawler_service
        self.__request_validator = request_validator

    def post(self, request):
        headers = request.data.get("headers", {})
        self.__request_validator.validate(request.data)
        request_data = RequestData(request.data["url"], request.data["list_selector"],
                                   request.data["selectors"], request.data["config"],
                                   headers)
        output = self.__crawler_service.crawl(request_data)
        return Response(output, status=status.HTTP_200_OK)
