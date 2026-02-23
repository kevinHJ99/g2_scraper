import random
import time


class Navigation:
    def __init__(self, config):
        self.config = config

    def build_targets(self):
        targets = []
        
        for _ in range(self.config.CYCLES):
            for category, pages in self.config.CATEGORIES.items():
                for num_pages in range(1, pages + 1):
                    targets.append((category, num_pages))
                    if len(targets) == self.config.MAX_ITERATIONS:
                        return targets

        return targets
    
    async def run(self, page, metrics, extractor, detector, storage, retry_execute):
        targets = self.build_targets()

        for i, (category, num_pages) in enumerate(targets, start=1):
            url = f"https://www.g2.com/categories/{category}?order=g2_score&page={num_pages}#product-list"

            s_time = time.time()

            print(f"{i} navegando en {url}")

            retries = 0
            response = None
            
            try:
                response, retries = await retry_execute.execute(page.goto, url, wait_until="networkidle")
                await page.wait_for_selector("#ajax-container", timeout=12000)

                x = random.randint(50, 400)
                y = random.randint(100, 600)

                await page.mouse.move(x, y)
                await page.wait_for_timeout(random.randint(500, 1200))
                await page.mouse.wheel(0, random.randint(300, 800))

                block_type = await detector.is_blocked(page, response)

                if block_type is not None:
                    raise Exception(block_type.value)
                
                html = await page.content()

                products = extractor.extract(html)
                storage.add_products(products, category)
                
                latency = time.time() - s_time

                metrics.record_ok(category, latency, retries=retries)

            except Exception as e:
                latency = time.time() - s_time
                metrics.record_error(category, str(e), latency, retries=retries)
            
            # random delay
            delay = random.uniform(*self.config.RANGE_DELAY)
            await page.wait_for_timeout(delay * 1000)