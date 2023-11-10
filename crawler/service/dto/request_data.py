from rest_framework import serializers


class RequestData:

    def __init__(self, url, list_selector, selectors, config, headers):
        self.url: str = url
        self.list_selector: str = list_selector
        self.selectors: dict = selectors
        self.config: dict = config
        self.headers: dict = headers

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url: str):
        if not isinstance(url, str):
            raise serializers.ValidationError('Invalid type of data in the "url" field')
        if not url.startswith('http'):
            raise serializers.ValidationError('Invalid value - the "url" field')
        self._url = url

    @property
    def list_selector(self):
        return self._list_selector

    @list_selector.setter
    def list_selector(self, list_selector: str):
        if not isinstance(list_selector, str):
            raise serializers.ValidationError('Invalid type of data in the "list_selector" field')
        self._list_selector = list_selector

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config: dict):
        if not isinstance(config, dict):
            raise ValueError('Invalid type of data in the "config" field')
        config_keys = config.keys()
        selectors_keys = self._selectors.keys()
        if not all([key in config_keys for key in selectors_keys]):
            raise serializers.ValidationError('Invalid value - the "config" field is missing required fields')
        self._config = config

    @property
    def selectors(self):
        return self._selectors

    @selectors.setter
    def selectors(self, selectors: dict):
        if not isinstance(selectors, dict):
            raise serializers.ValidationError('Invalid type of data in the "selectors" field')
        for key, value in selectors.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise serializers.ValidationError('Invalid type of data in the "selectors" field')
        self._selectors = selectors

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, headers: dict):
        if not isinstance(headers, dict):
            raise ValueError('Invalid type of data in the "headers" field')
        self._headers = headers
