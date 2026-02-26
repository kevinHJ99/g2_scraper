# G2 Scraper
===========

Scraper de G2 con Playwright conectado a Chrome via CDP (Chrome DevTools Protocol).

## Requisitos
-----------
- Python 3.10+.
- Google Chrome instalado (se usa CDP en el puerto 9222).
- Windows/macOS/Linux.

## Estructura
├───G2_scraper
    │   config.py
    │   main.py
    │   README.md
    |   METRICS_REPORT.md
    |   REPORT.md
    |   requirements.txt
    │
    ├───source
    │       browser.py
    │       detector.py
    │       extractor.py
    │       metrics.py
    │       navigator.py
    │       retries.py
    │	    run_chrome.py
    │
    ├───data
    └───logs

## Clonar desde GitHub
-------------------
1) Clona el repositorio:

```bash
git clone https://github.com/USUARIO/REPO.git
cd REPO/G2_scraper
```

2) Crea y activa un entorno virtual:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3) Instala dependencias:

```bash
pip install -r requirements.txt
```

Estructura del proceso
----------------------
1) Chrome CDP: se inicia Chrome en el puerto 9222 (ver [src/run_chrome.py](src/run_chrome.py)).
2) Conexión CDP: Playwright se conecta a Chrome (ver [src/browser.py](src/browser.py)).
3) Warmup: navegación inicial y comportamiento humano simulado (ver [src/navigator.py](src/navigator.py)).
4) Iteraciones: se recorren categorias y paginas (ver [config.py](config.py)).
5) Detección de bloqueo: validación de señales de bloqueo (ver [src/detector.py](src/detector.py)).
6) Extracción: parseo de HTML con XPath (ver [src/extractor.py](src/extractor.py)).
7) Persistencia: se guarda JSON y CSV (ver [src/file_storage.py](src/file_storage.py)).

Ejecución
---------
1) Asegura que Chrome CDP esté listo (se inicia automáticamente al correr el script).
2) Ejecuta el scraper:

```bash
python main.py
```

Configuración
-------------
Edita [config.py](config.py) para controlar:
- Iteraciones y retrasos (`MAX_ITERATIONS`, `RANGE_DELAY`).
- Categorias y paginas (`CATEGORIES`).
- Endpoint CDP (`ENDPOINT_URL`).

Salida
------
- Datos: [data/products.json](data/products.json) y [data/products.csv](data/products.csv).
- Logs: [logs/metrics_summary.json](logs/metrics_summary.json).

Notas
-----
- Si cambias el puerto CDP, actualiza `ENDPOINT_URL`.
- Si Chrome no inicia, revisa la ruta del ejecutable en [src/run_chrome.py](src/run_chrome.py).
- Corregida la ruta de chrome para la ejecucion, se uso la libreria shutil y winreg