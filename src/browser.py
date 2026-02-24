from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import logging

class BrowserManager:
    def __init__(self, playwright, endpoint_url):
        self.playwright = playwright
        self.endpoint_url = endpoint_url

    async def create(self):
        try:
            # inicializa playwright
            browser = await self.playwright.chromium.connect_over_cdp(self.endpoint_url, timeout=60000)
            
            # crear un nuevo contexto y página del navegador
            context = browser.contexts[0]

            if context.pages:
                page = context.pages[0]
            else:
                page = await context.new_page()

            return page
        except Exception as e:
            logging.error(f"Error creating browser: {e}")