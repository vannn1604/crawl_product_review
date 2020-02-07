import scrapy
from ..items import ReviewItem


class ReviewsSpider(scrapy.Spider):
    name = "review"
    allowed_domains = ["www.gsmarena.com"]
    start_urls = ["https://www.gsmarena.com/makers.php3"]

    def parse(self, response):
        for a in response.xpath('//*[@id="body"]/div/div[2]/table/tr/td/a'):
            yield response.follow(
                a, callback=self.parse_brand, cb_kwargs={"brand": a.xpath("./text()").get()}
            )

    def parse_brand(self, response, brand):
        for product in response.xpath('//*[@id="review-body"]/div[1]/ul/li/a'):
            yield response.follow(
                product,
                callback=self.parse_product,
                cb_kwargs={"name": product.xpath("./strong/span/text()").get(), "brand": brand},
            )

        for a in response.xpath('//a[@class="pages-next"]'):
            yield response.follow(a, callback=self.parse_brand, cb_kwargs={"brand": brand})

    def parse_product(self, response, name, brand):
        for product in response.xpath('//*[@id="user-comments"]/div[4]/div[1]/ul/li[1]/a'):
            yield response.follow(
                product, callback=self.parse_review, cb_kwargs={"name": name, "brand": brand},
            )

    def parse_review(self, response, name, brand):
        for div in response.xpath('//div[@class="user-thread"]'):
            username = div.xpath("./ul[1]/li[1]/text()").get()
            if username is None:
                username = div.xpath("./ul[1]/li[1]/a/b/text()").get()

            review = {
                "username": username,
                "time": div.xpath("./ul[1]/li[3]/time/text()").get(),
                "content": div.xpath("./p/text()").get(default="").strip(),
                "rating": div.xpath("./ul[2]/li[1]/span[2]/text()").get(),
                "location": div.xpath("./ul[1]/li[2]/span/text()").get(),
            }
            yield ReviewItem(brand=brand, name=name, review=review)

        for a in response.xpath('//a[@title="Next page"]'):
            yield response.follow(
                a, callback=self.parse_review, cb_kwargs={"name": name, "brand": brand},
            )


"""
    def parse_review(self, response, name, brand, reviews):
        for div in response.xpath('//div[@class="user-thread"]'):
            username = div.xpath("./ul[1]/li[1]/text()").get()
            if username is None:
                username = div.xpath("./ul[1]/li[1]/a/b/text()").get()

            review = {
                "username": username,
                "time": div.xpath("./ul[1]/li[3]/time/text()").get(),
                "content": div.xpath("./p/text()").get(default="").strip(),
                "rating": div.xpath("./ul[2]/li[1]/span[2]/text()").get(),
                "location": div.xpath("./ul[1]/li[2]/span/text()").get(),
            }
            reviews.append(review)

        if not response.xpath('//a[@title="Next page"]'):
            yield ReviewItem(brand=brand, name=name, reviews=reviews)

        for a in response.xpath('//a[@title="Next page"]'):
            yield response.follow(
                a,
                callback=self.parse_review,
                cb_kwargs={"name": name, "brand": brand, "reviews": reviews},
            )
"""

