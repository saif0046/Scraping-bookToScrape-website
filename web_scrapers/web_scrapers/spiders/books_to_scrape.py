import scrapy


class BooksToScrapeSpider(scrapy.Spider):
    name = "books_to_scrape"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response, **kwargs):
        for next_page in response.xpath('//*[@id="default"]/div/div/div/div/section/div[2]/ol/li/article/div[1]/a'):
            next_page = next_page.xpath('.//@href').get()
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.meta_data
            )

        next_pagination = response.xpath('.//li[@class="next"]/a/@href').get()
        if next_pagination:
            yield scrapy.Request(
                url=response.urljoin(next_pagination),
                callback=self.parse
            )

    def meta_data(self, response):
        book_image = response.xpath('//*[@id="product_gallery"]/div/div/div/img/@src').get()
        book_image = response.urljoin(book_image)

        kwargs = {
            "Product_Info": {
                "UPC": response.xpath('//*[@id="content_inner"]/article/table/tr[1]/td/text()').get(),
                "Product Type": response.xpath('.//tr[2]/td/text()').get(),
                "Price (excl. tax)": response.xpath('.//tr[3]/td/text()').get(),
                "Price (incl. tax)": response.xpath('.//tr[4]/td/text()').get(),
                "Tax": response.xpath('.//tr[5]/td/text()').get(),
                "Availability": response.xpath('.//tr[6]/td/text()').get(),
                "Number of reviews": response.xpath('.//tr[7]/td/text()').get()
            },
            "book_data": {
                'book_name': response.xpath('//*[@id="content_inner"]/article/div[1]/div[2]/h1/text()').get(),
                'book_price': response.xpath('.//p[1]/text()').get(),
                'book_rating': response.xpath('.//p[contains(@class, "star-rating")]/@class').get().split()[-1],
                'book_image': book_image,
                'book_url': response.url
            }
        }
        yield kwargs
