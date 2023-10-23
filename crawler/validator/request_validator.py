import re

from rest_framework import serializers


class RequestValidator:
    def validate(self, request_data):
        self.__validate_all_keys_exist(request_data)
        self.__validate_url(request_data["url"])
        self.__validate_list_selector(request_data["list_selector"])
        self.__validate_selectors(request_data["selectors"])
        self.__validate_config(request_data)

    @staticmethod
    def __validate_all_keys_exist(request_data):
        if not all([request_data.get('url'), request_data.get('list_selector'), request_data.get('selectors'),
                    request_data.get('config')]):
            raise serializers.ValidationError('Missing field key in request data')

    def __validate_values(self, request_data):
        self.__validate_url(request_data.url)
        self.__validate_list_selector(request_data.list_selector)
        self.__validate_selectors(request_data.selectors)

    def __validate_url(self, url):
        if not isinstance(url, str):
            raise serializers.ValidationError('Invalid type of data in the "url" field')
        if not url.startswith('http'):
            raise serializers.ValidationError('Invalid value - the "url" field')


    def __validate_config(self, request_data):
        config_keys = request_data.get('config').keys()
        selectors_keys = request_data.get('selectors').keys()
        if not all([key in config_keys for key in selectors_keys]):
            raise serializers.ValidationError('Invalid value - the "config" field is missing required fields')




    def __validate_list_selector(self, list_selector):
        if not isinstance(list_selector, str):
            raise serializers.ValidationError('Invalid type of data in the "list_selector" field')

    def __validate_selectors(self, selectors):
        if not isinstance(selectors, dict):
            raise serializers.ValidationError('Invalid type of data in the "selectors" field')
        for key, value in selectors.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise serializers.ValidationError('Invalid type of data in the "selectors" field')
