from lxml import html

class ExtractProducts:
    def __init__(self, products=5):
        self.products = products

    def extract(self, html):
        dom = html.fromstring(html)

        self.items = dom.xpath('//div[@itemprop="itemListElement"]')

        self.products = []

        for item in self.items:
            name = item.xpath('.//div[@class="product-card__product-name"]/text()')
            description = item.xpath('.//div[contains(@id, "-overview-page")]/text()')
            ratings = item.xpath('//span[contains(@class, "fw-semibold")]//preceding-sibling::span/text()')
            seller = None
            seller = None
            link = None

    