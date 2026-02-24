from lxml import html

class ExtractProducts:
    def __init__(self, min_products=10):
        self.min_products = min_products

    def extract(self, html_content):
        dom = html.fromstring(html_content)

        self.items = dom.xpath('//div[@itemprop="itemListElement"]')
        self.products_list = []

        for item in self.items[:self.min_products]:
            sponsored = item.xpath('.//*[contains(text(), "Sponsored")]/text()')
            if sponsored:
                continue
            name = item.xpath('.//div[@class="product-card__product-name"]//div/text()')
            Users = item.xpath('.//div[contains(text(), "Users")]/following-sibling::ul//text()')
            industries = item.xpath('.//div[contains(text(), "Industries")]/following-sibling::ul//text()')
            ratings = item.xpath('.//span[contains(@class, "fw-semibold")]//preceding-sibling::span/text()')
            seller = item.xpath('.//a[@data-test-id="tracked-seller-page-link"]/text()')
            link = item.xpath('.//div[@class="product-card__product-name"]/a/@href')

            self.products_list.append({
                'name': name[0] if name else None,
                'ratings': float(ratings[0]) if ratings else None,
                'seller': seller[0] if seller else None,
                'users': Users if Users else None,
                'industries': industries if industries else None,
                'link': link[0] if link else None
            })

        self.validate(self.products_list)

        return self.products_list
    
    def validate(self, product):
        if len(product) < self.min_products:
            raise ValueError("Productos insuficientes detectados. - Posible Bloqueo")