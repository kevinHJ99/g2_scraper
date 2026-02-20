import logging
import random
import time


class Navigation:
    def __init__(self, page, config):
        self.page = page
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
    
    async def run(self, page, metrics):
        targets = self.build_targets()

        for i, (category, num_pages) in enumerate(targets, start=1):
            url = f"https://www.g2.com/categories/{category}?order=g2_score&page={num_pages}#product-list"

            s_time = time.time()

            print(f"{idx} navegando en {url}")

            try:
                await self.page.goto(url, timeout=self.config.TIMEOUT, wait_until="networkidle")
                await self.page.wait_for_selector("#ajax-container", timeout=12000)

                if detector.is_blocked:
                    raise Exception("Blocked detected")
                
                latency = time.time() - s_time
                metrics.record_navigation(category, latency)

            except Exception as e:
                latency = time.time() - s_time
                metrics.record_error(category, str(e), latency)
            
            # random delay
            delay = random.uniform(self.config.RANGE_DELAY)
            await self.page.wait_for_timeout(delay * 1000)