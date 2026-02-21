from playwright.async_api import async_playwright

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
            # initialize the playwright and launch the browser
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=self.headless)
            
            # create a new browser context and page
            self.context = await self.browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent=self.user_agent,)
            
            # create a new page in the browser context
            self.page = await self.context.new_page()
            return self.page
        except Exception as e:
            print(f"Error starting browser: {e}")
            await self.stop()
    
    async def stop(self):
        try:
            # close the browser and stop the playwright
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
        except Exception as e:
            print(f"Error stopping browser: {e}")