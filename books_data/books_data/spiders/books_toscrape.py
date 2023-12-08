"""
Created on Fri Dec  8 17:00:04 2023

@author: AusKing: ausking106710@gmail.com
"""

import scrapy
import json


def insert_into_json(path, data):
    with open(path, 'a') as json_file:
        json.dump(data, json_file, indent=4)
        
class BooksToscrapeSpider(scrapy.Spider):
    name = "books_toscrape"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]
    
    def start_requests(self):
        urls = [
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = f"file-books_toscrape-{page}.json"
        
        for book_ in response.css(".product_pod"):
            
            book_name = book_.css("h3 a::text").get()
            book_image = book_.css(".image_container img").attrib['src']
            book_rating = book_.css(".star-rating").attrib['class'].split(' ')[-1]
            book_price = book_.css(".price_color::text").get().replace('\u00a3', 'British Pound ')
            # you can use one of those method
            book_availability = book_.css(".instock i").attrib['class'].split('-')[-1]
            # or
            #book_availability = book_.css(".instock::text").getall()[-1].replace(' ', '').replace('\n', '')
            # or(highly not recommended)
            #if len(book_.css(".instock .icon-ok")) > 0:
                #book_availability = True
            #else:
                #book_availability = False
                
            book_data = {'book_name': book_name, 'book_image': book_image, 'book_rating': book_rating, 'book_price': book_price, 'book_availability': book_availability}
            
            insert_into_json(filename, book_data)
                
            
# Run command > scrapy crawl books_toscrape            