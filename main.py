import config
import asyncio
import json

from src.browser import BrowserManager as Browser
from src.navigator import Navigation
from src.metrics import MetricsRecorder
from src.detector import Detector
from src.retries import Retry
from src.file_storage import FileStorageManager
from src.extractor import ExtractProducts

async def main():

    # ===============// Iniciar Navegador //==============
    browser_manager = Browser(config.HEADLESS, config.USER_AGENT)
    page = await browser_manager.start()

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

    # ===============// Guardar Datos //==============
    storage.save_json()
    storage.save_csv()

    # ===============// Guardar Metricas //==============
    summary_ = metrics.summary()
    for key, value in summary_.items():
        print(f"{key}: {value}")

    with open('logs/metrics_summary.json', 'w') as f:
        json.dump(summary_, f, indent=4)

    # ===============// Cerrar Navegador //==============
    await browser_manager.stop()

if __name__ == "__main__":
    asyncio.run(main())