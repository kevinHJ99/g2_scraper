import config
import asyncio
import json
import logging
from playwright.async_api import async_playwright

from src.browser import BrowserManager as Browser
from src.navigator import Navigation
from src.metrics import MetricsRecorder
from src.detector import Detector
from src.retries import Retry
from src.file_storage import FileStorageManager
from src.extractor import ExtractProducts
from src.run_chrome import ChromeManager

async def main():

    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
    )

    # ===============// Iniciar Chrome CDP //==============
    ChromeManager.ensure_chrome()
    logging.info("Chrome CDP iniciado en el puerto 9222")

    # ===============// Iniciar Navegador //==============
    async with async_playwright() as p:
        browser_manager = Browser(p, config.ENDPOINT_URL)
        page = await browser_manager.create()

        # ===============// Instanciar Componentes //==============
        navigator = Navigation(config)
        detector = Detector()
        metrics = MetricsRecorder()
        extractor = ExtractProducts()
        storage = FileStorageManager('data')
        retry_execute = Retry(config.MAX_RETRIES, config.DELAY_MIN)

        # ===============// Executar Navegador //==============
        await navigator.warmup(page)
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
        logging.info(f"{key}: {value}")

    with open('logs/metrics_summary.json', 'w') as f:
        json.dump(summary_, f, indent=4)
   
    # ===============// Guardar Datos //==============
    storage.save_json()
    storage.save_csv()

    logging.info(storage.get_stats())

if __name__ == "__main__":
    asyncio.run(main())