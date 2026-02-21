import config
import asyncio

from src.browser import Browser
from src.navigator import Navigation
from src.metrics import MetricsRecorder
from src.detector import Detector

async def main():

    # ===============// Iniciar Navgeador //==============
    broswer_manager = Browser(config.HEADLESS, config.USER_AGENT)
    page = await broswer_manager.start()

    # ===============// Instanciar Componentes //==============
    navigator = Navigation(config)
    detector = Detector()
    metrics = MetricsRecorder()

    # ===============// Executar Navegador //==============
    await navigator.run(page, detector, metrics)

    summary_ = metrics.summary()
    for key, value in summary_.items():
        print(f"{key}: {value}")

    # ===============// Cerrar Navegador //==============
    await broswer_manager.stop()

if __name__ == "__main__":
    asyncio.run(main())