Reporte

-> Durante el desarrollo del motor de scraping para g2.com, se identificó que el sitio utiliza mecanismos avanzados de protección contra scraping y bots, incluyendo:

* Cloudflare
* DataDome (Activo)
* Fingerprinting del navegador y sistema operativo
* Evaluación progresiva de sesión
* Challenge dinámico vía JavaScript

=================================
Se eligio Playwright como la herramienta mejor alternativa para realizar el scraper.
Sin embargo, estos mecanismos detectan entornos automatizados, especialmente navegadores en contenedores o perfiles limpios.

Intentos realizados:

-> Se evaluaron múltiples configuraciones:

* Playwright con Chromium embebido
→ Bloqueo inmediato.

* Playwright + Stealth
→ No mitigó la detección.

* Browserless en Docker
→ Home funcional, bloqueo en navegación a categorías (Js Challenge).

* Chrome en contenedor Debian
→ Persistencia de fingerprint Linux detectable (Redireccion a una pagina de bloqueo o Js Challenge).

Conclusión:
Los entornos Linux en contenedor generan señales detectables por los sistemas anti-bot del sitio, usar playwright estandar
es facilmente detectable.

===================================
Solución adoptada

-> Se implementó una arquitectura basada en:

Chrome real del sistema controlado vía CDP
Chrome externo (Chrome DevTools Protoco)

Razon:

* Fingerprint humano real (OS, GPU, fuentes, historial)

* Perfil y cookies persistentes

* Mayor estabilidad frente a detección progresiva

* Renderizado desacoplado de la lógica de scraping

==================================

Arquitectura final

-> El motor implementa:

* Conexión CDP a navegador externo

* Navegación controlada por ciclos

* Extractor robusto con validación mínima

* Detector de challenge

* Retry con backoff exponencial

-> Registro de métricas:

* Tasa de éxito

* Latencia promedio

* Manejo de excepciones

* Conteo de bloqueos

* Tipo de Bloqueos

-> El sistema es escalable a futuro hacia:

* Browserless SaaS

* Proxies residenciales

* Contendores en docker con Browser farm

============================================

-> Porque Playwright y no Selenium
- Selenium usa el protocolo WebDriver, que envía comandos HTTP por cada interacción. Es más lento y propenso a latencia.
- Selenium requiere de waits manuales para evitar errores de elementos no encontrados.
- Playwright puede usar el Chrome DevTools Protocol (CDP), una conexión WebSocket bidireccional constante. Esto permite una comunicación casi instantánea y un control mucho más granular sobre el navegador (ideal para entornos externos en Docker).
- Playwright es nativamente asincrono, lo que permite esperas automaticas sobre la carga los items antes de ejecutar una accion.

===========================================

-> Nota de extraccion:
Algunos campos presentan valores nulos debido a que la información no está disponible en el DOM del listado, no por fallo del extractor.

===========================================
Conclusión

El entorno del sitio está diseñado para detectar automatización en entornos no humanos.
El renderizado es gestionado por una instancia externa de Chrome real, conectada vía CDP, dado que el uso de servidores
externos con entornos limpios son detectados por el fingerprint o el challenge de Js.
Esto permite desacoplar completamente la lógica del scraper del motor de renderizado, garantizando intercambiabilidad y resiliencia.