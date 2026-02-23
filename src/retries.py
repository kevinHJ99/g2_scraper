import asyncio
import random

class Retry:
    def __init__(self, retries=3, delay=5):
        self.retries = retries
        self.delay = delay

    async def execute(self, cor_func, *args, **kwargs):

        last_exception = None

        for attempt in range(1, self.retries + 1):
            try:
                result = await cor_func(*args, **kwargs)
                return result, attempt - 1 # Reintentos realizados
            except Exception as e:
                last_exception = e

                if attempt < self.retries:
                    delay_time = self.delay * (2 ** (attempt - 1)) + random.uniform(0.5, 1.5)
                    await asyncio.sleep(delay_time)
                elif attempt == self.retries:
                    raise last_exception
                else:
                    print("All retry attempts failed.")
                    raise last_exception