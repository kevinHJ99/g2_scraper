from lxml import html

class ExtractProducts:
    def __init__(self, min_products=5):
        self.min_products = min_products

    def extract(self, html_content):
        dom = html.fromstring(html_content)

        self.items = dom.xpath('//div[@itemprop="itemListElement"]')
        self.products_list = []

        for item in self.items[:self.min_products]:
            sponsored = item.xpath('.//div[@class="elv-text-subtle elv-font-bold"]/text()')
            if sponsored and "Sponsored" in sponsored[0]:
                continue
            name = item.xpath('.//div[@class="product-card__product-name"]/text()')
            description = item.xpath('.//div[contains(@id, "-overview-page")]//div[@data-nosnippet]//span[@class="hide-if-js"]/text()')
            ratings = item.xpath('.//span[contains(@class, "fw-semibold")]//preceding-sibling::span/text()')
            seller = item.xpath('.//a[@data-test-id="tracked-seller-page-link"]/child::span/text()')
            link = item.xpath('.//a[@data-test-id="product-card-link"]/@href')

            self.products_list.append({
                'name': name[0] if name else None,
                'description': description[0] if description else None,
                'ratings': float(ratings[0]) if ratings else None,
                'seller': seller[0] if seller else None,
                'link': link[0] if link else None
            })

        self.validate(self.products_list)

        return self.products_list
    
    def validate(self, product):
        if len(product) < self.min_products:
            raise ValueError("Productos insuficientes detectados. - Posible Bloqueo")