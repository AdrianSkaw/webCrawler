import re

from rest_framework import serializers


class RequestValidator:
    def validate(self, request_data):
        self.__validate_all_keys_exist(request_data)

    @staticmethod
    def __validate_all_keys_exist(request_data):
        if not all([request_data.get('url'), request_data.get('list_selector'), request_data.get('selectors'),
                    request_data.get('config')]):
            raise serializers.ValidationError('Missing field key in request data')














