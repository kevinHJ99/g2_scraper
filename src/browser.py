from playwright.async_api import async_playwright
from playwright_stealth import Stealth
import logging

class BrowserManager:
    def __init__(self, headless: bool = False, user_agent: str = None):
        self.headless = headless
        self.user_agent = user_agent
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        try:
            # inicializa playwright
            self.playwright = await async_playwright().start()
            async with Stealth().use_async(self.playwright) as p:
                self.browser = await p.chromium.launch(
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
                self.context = await self.browser.new_context(
                    viewport={"width": 1280, "height": 800},
                    user_agent=self.user_agent,)
                
                # crear una nueva página en el contexto del navegador
                self.page = await self.context.new_page()

                return self.page
        except Exception as e:
            logging.error(f"Error starting browser: {e}")
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