Contexto

-> Durante el desarrollo del motor de scraping para g2.com, se identificó que el sitio utiliza mecanismos avanzados de protección contra automatización, incluyendo:

* Cloudflare
* DataDome (Activo)
* Fingerprinting del navegador y sistema operativo
* Evaluación progresiva de sesión
* Challenge dinámico vía JavaScript

=================================
Estos mecanismos detectan entornos automatizados, especialmente navegadores en contenedores o perfiles limpios.

Intentos realizados

-> Se evaluaron múltiples configuraciones:

* Playwright con Chromium embebido
→ Bloqueo inmediato.

* Playwright + Stealth
→ No mitigó la detección.

* Browserless en Docker
→ Home funcional, bloqueo en navegación a categorías.

* Chrome en contenedor Debian
→ Persistencia de fingerprint Linux detectable.

Conclusión:
Los entornos Linux en contenedor generan señales detectables por los sistemas anti-bot del sitio.

===================================
Solución adoptada

-> Se implementó una arquitectura basada en:

Chrome real del sistema controlado vía CDP
Chrome externo (CDP)
        ↓
Motor de Scraping desacoplado

Ventajas:

* Fingerprint humano real (OS, GPU, fuentes, historial)

* Perfil persistente

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

-> El sistema es escalable a futuro hacia:

* Browserless SaaS

* Proxies residenciales

* Infraestructura distribuida

Conclusión

El entorno del sitio está diseñado para detectar automatización en entornos no humanos.
La solución implementada maximiza estabilidad manteniendo desacople arquitectónico y escalabilidad, sin introducir infraestructura externa innecesaria para el alcance de la prueba.