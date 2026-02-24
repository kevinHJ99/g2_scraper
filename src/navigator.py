import random
import logging
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
    
    async def warmup(self, page):
        await page.goto("https://www.g2.com", wait_until="domcontentloaded")
        await page.wait_for_timeout(4000)

        for _ in range(random.randint(2, 4)):
            await page.mouse.wheel(0, random.randint(300, 800))
            await page.wait_for_timeout(random.randint(800, 1500))
        
        for _ in range(random.randint(2, 4)):
            await page.mouse.wheel(0, random.randint(200, 600))
            await page.wait_for_timeout(random.randint(800, 1500))

        for _ in range(random.randint(2, 4)):
            await page.mouse.wheel(0, random.randint(200, 600))
            await page.wait_for_timeout(random.randint(800, 1500))

    
    async def run(self, page, metrics, extractor, detector, storage, retry_execute):
        targets = self.build_targets()

        for i, (category, num_pages) in enumerate(targets, start=1):
            if i % 10 == 0:
                await page.wait_for_timeout(random.randint(10000, 15000))  # pausa cada 10 iteraciones

            url = f"https://www.g2.com/categories/{category}?page={num_pages}"

            s_time = time.time()

            logging.info(f"{i} navegando en {url}")

            retries = 0
            response = None
            
            try:
                response, retries = await retry_execute.execute(page.goto, url, wait_until="domcontentloaded")
                await page.wait_for_selector('div[id="product-cards"]', state="attached", timeout=12000)

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

                logging.info(f"[Iter {i}] Productos: {len(products)} | HTML size: {len(html)}")
                
                latency = time.time() - s_time

                logging.info(f"[Iter {i}] Latencia: {round(latency, 2)}s | Retries: {retries}")

                metrics.record_ok(category, latency, retries=retries)

            except Exception as e:
                latency = time.time() - s_time
                metrics.record_error(category, str(e), latency, retries=retries)
                logging.error(f"Error en {url}: {e}")
            
            # random delay
            delay = random.uniform(*self.config.RANGE_DELAY)
            await page.wait_for_timeout(delay * 1000)