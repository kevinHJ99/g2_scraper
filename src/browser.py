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
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-accelerated-2d-canvas",
                    "--disable-gpu",
                    "--window-size=1280,800"
                ]
                )
            
            # crear un nuevo contexto y página del navegador
            context = await self.browser.new_context(viewport={"width": 1280, "height": 800},)
            
            # crear una nueva página en el contexto del navegador
            page = await context.new_page()

            return page
        except Exception as e:
            logging.error(f"Error creating browser: {e}")
            await self.stop()

    async def stop(self):
        try:
            # cerrar el navegador y detener playwright
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
        except Exception as e:
            logging.error(f"Error stopping browser: {e}")