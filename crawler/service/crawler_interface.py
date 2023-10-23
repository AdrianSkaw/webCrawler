import abc


class CrawlerInterface(abc.ABC):

    @abc.abstractmethod
    def get_attribute(self, element, xpath_price, atribute):
        pass

    @abc.abstractmethod
    def find_elements(self, web_session, xpath):
        pass

    @abc.abstractmethod
    def get_text(self, element, xpath_price, nullable):
        pass

    @abc.abstractmethod
    def create_web_session(self, url, headers):
        pass

    @abc.abstractmethod
    def crawl(self, request_data):
        pass


    