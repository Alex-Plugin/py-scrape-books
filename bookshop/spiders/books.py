from pathlib import Path

import scrapy
from scrapy.http import Response


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    RATING_MAP = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
    }

    def convert_rating(self, rating_text):
        return self.RATING_MAP.get(rating_text)


    def parse(self, response: Response, **kwargs):
        for book in response.css("article.product_pod"):
            rating_text = book.css("p.star-rating::attr(class)").get().split()[-1]
            yield {
                "title": book.css("h3 a::attr(title)").get(),
                "price": float(book.css(".price_color::text").get().replace("£", "")),
                "rating": int(self.convert_rating(rating_text))
            }



