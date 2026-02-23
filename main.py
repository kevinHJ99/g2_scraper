import config
import asyncio
import json
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

from src.browser import BrowserManager as Browser
from src.navigator import Navigation
from src.metrics import MetricsRecorder
from src.detector import Detector
from src.retries import Retry
from src.file_storage import FileStorageManager
from src.extractor import ExtractProducts

async def main():

    # ===============// Iniciar Navegador //==============
    async with Stealth().use_async(async_playwright()) as p:
        browser_manager = Browser(p, config.HEADLESS, config.USER_AGENT)
        page = await browser_manager.create()

        # ===============// Instanciar Componentes //==============
        navigator = Navigation(config)
        detector = Detector()
        metrics = MetricsRecorder()
        extractor = ExtractProducts()
        storage = FileStorageManager('data')
        retry_execute = Retry(config.MAX_RETRIES, config.INITIAL_BACKOFF)

        # ===============// Executar Navegador //==============
        await navigator.run(
            page, 
            metrics, 
            extractor,
            detector, 
            storage, 
            retry_execute
            )

        # ===============// Guardar Metricas //==============
        summary_ = metrics.summary()
        for key, value in summary_.items():
            print(f"{key}: {value}")

        with open('logs/metrics_summary.json', 'w') as f:
            json.dump(summary_, f, indent=4)
   
    # ===============// Guardar Datos //==============
    storage.save_json()
    storage.save_csv()

if __name__ == "__main__":
    asyncio.run(main())