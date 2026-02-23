from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import logging

class BrowserManager:
    def __init__(self, playwright, headless: bool = False, user_agent: str = None):
        self.playwright = playwright
        self.headless = headless
        self.user_agent = user_agent

    async def create(self):
        try:
            # inicializa playwright
            self.context = await self.playwright.chromium.launch_persistent_context(
                headless=self.headless,
                viewport={"width": 1280, "height": 800},
                locale="es-CO",
                timezone_id="America/Bogota",
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-accelerated-2d-canvas",
                    "--disable-gpu",
                    "--window-size=1280,800",
                ]
                )
            
            # crear un nuevo contexto y página del navegador
            # context = await self.browser.new_context(viewport={"width": 1280, "height": 800},)
            
            # crear una nueva página en el contexto del navegador
            page = await self.context.new_pages()[0]

            return page
        except Exception as e:
            logging.error(f"Error creating browser: {e}")
            await self.stop()