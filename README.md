# Web Stories Data Scraping Service

This is a service designed for scraping data from web stories. It provides an API endpoint that accepts a URL, list selector, and configuration details for extracting specific data from the given webpage.

Service created by Adrian Skawinski

Stack:

- Python3
- Docker-Compose
- Django
- Django Rest Framework
- Pydantic
- Celery
- Redis
- Dependency injection
- SQLite3

## Setup Instructions


Developing
----------

### Init environment ###

Execute command in project dir:

    docker-compose up --build

run app 
    
    docker-compose run web_crawler python manage.py runserver


POST http://127.0.0.1:8000/api/v1/crawler


### Request Body
```json
{
    "url": "https://www.komputronik.pl/category/1251/monitory.html",
    "list_selector": "div[ng-if=\"!$ctrl.isFiltered && $ctrl.productsCount > 0\"] div[class=\"tests-product-entry\"]",
    "config": {
        "title": {"allow_missing": false},
        "price": {"allow_missing": false},
        "url": {"allow_missing": false, "attribute": "href"}
    },
    "selectors": {
        "title": "h2[class=\"font-headline text-lg font-bold leading-6 line-clamp-3 md:text-xl md:leading-8\"] a",
        "url": "h2[class=\"font-headline text-lg font-bold leading-6 line-clamp-3 md:text-xl md:leading-8\"] a",
        "price": "div[class=\"text-3xl font-bold leading-8\"]"
    }
}
```
Description:

- `url`: The URL of the webpage to be scraped.
  - `list_selector`: CSS selector for identifying the list of items on the webpage.
  - `config`: Configuration settings for data extraction.
      - `title`, `price`, `url`: Configuration for each data field.
          - `allow_missing`: Whether the field is required (set to `false`).
          - `attribute` (optional): Attribute to extract (e.g., `"href"` for links).
  - `selectors`: CSS selectors for extracting individual data fields (`title`, `url`, `price`).

Replace the example URL and selectors with your desired values to scrape data from different webpages.
