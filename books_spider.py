# bookscraper/spiders/books_spider.py
import scrapy

class BooksSpider(scrapy.Spider):
    name = 'books_spider'
    start_urls = ['http://books.toscrape.com']
    scraped_items = 0
    MAX_ITEMS = 750  #Setting the max items to 750 as per the constraints.

    def parse(self, response):
        # Extract book information
        for book in response.css('article.product_pod h3 a::attr(href)').getall():
            yield scrapy.Request(response.urljoin(book), callback=self.parse_book)

            # Check if the maximum number of items has been reached
            if self.scraped_items >= self.MAX_ITEMS:
                self.log(f'Stopping spider after scraping {self.MAX_ITEMS} items.')
                return

        # Follow pagination links
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_book(self, response):
        # Extract detailed book information
        yield {
            'title': response.css('h1::text').get(),
            'price': response.css('p.price_color::text').get(),
            'image_url': response.css('img::attr(src)').get(),
            'details_url': response.url
        }

        # Increment the counter
        self.scraped_items += 1

    def closed(self, reason):
        self.log(f'Spider closed because: {reason}')
