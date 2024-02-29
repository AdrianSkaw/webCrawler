from django.apps import AppConfig


class CrawlerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crawler'

    def ready(self):
        from crawler.di.base_container import BaseContainer

        base_container = BaseContainer()
        base_container.wire(modules=["crawler.views"
                                     ])
