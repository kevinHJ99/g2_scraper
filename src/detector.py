from enum import Enum

class BlockType(Enum):
    CLOUD_FLARE = "Cloudflare"
    CAPTCHA = "Captcha"
    DATA_DOME = "Datadome"
    DOM_ERROR = "DOM Error"
    RATE_LIMIT = "Rate Limit"
    BAD_RESPONSE = "Bad Response"
    BAD_REQUEST = "Bad Request"
    IP_BLOCK = "IP Block"
    REDIRECTS = "Redirects"
    SOFT_BLOCK = "Soft Block"

class Detector:
    
    async def is_blocked(self, page):
        """
        Evalua multiples senales o indicadores de bloqueo.
        Retorna True si detecta Bloqueo.
        """
        if await self.detect_cloudflare(page):
            print("Cloudflare detected")
            return BlockType.CLOUD_FLARE
        if await self.detect_captcha(page):
            print("Captcha detected")
            return BlockType.CAPTCHA
        if await self.detect_datadome(page):
            print("Datadome detected")
            return BlockType.DATA_DOME
        if await self.detect_dom_error(page):
            print("DOM error detected")
            return BlockType.DOM_ERROR
        if await self.detect_rate_limit(page):
            print("Rate limit detected")
            return BlockType.RATE_LIMIT
        if await self.bad_response(page):
            print("Bad response detected")
            return BlockType.BAD_RESPONSE
        if await self.bad_request(page):
            print("Bad request detected")
            return BlockType.BAD_REQUEST
        if await self.detect_ip_block(page):
            print("IP block detected")
            return BlockType.IP_BLOCK
        if await self.detect_redirects(page):
            print("Suspicious redirects detected")
            return BlockType.REDIRECTS
        if await self.soft_block(page):
            print("Soft block detected")
            return BlockType.SOFT_BLOCK

    async def detect_cloudflare(self, page):
        """
        Detecta si la pagina esta protegida por Cloudflare.
        Retorna True si detecta Cloudflare.
        """
        if "cdn-dgi" in page.url:
            return True
        
        content = await page.content()
        if "challenge-form" in content or "cf-ray" in content:
            return True

    async def detect_captcha(self, page):
        """
        Detecta si la pagina esta protegida por un Captcha.
        Retorna True si detecta un Captcha.
        """
        content = await page.content()
        if "captcha" in content.lower() or "g-recaptcha" in content:
            return True
        

    async def detect_datadome(self, page):
        """
        Detecta si la pagina esta protegida por Datadome.
        Retorna True si detecta Datadome.
        """
        content = await page.content()
        if "datadome" in content.lower():
            return True

    async def detect_dom_error(self, page):
        """
        Detecta errores en el DOM que puedan indicar bloqueo.
        Retorna True si detecta errores en el DOM.
        """
        content = await page.query_selector("#ajax-container")
        if content is None:
            return False
        
        if "blocked" in await content.inner_text().lower():
            return True

    async def detect_rate_limit(self, page):
        """
        Detecta si la pagina esta aplicando limitacion de tasa (Rate Limiting).
        Retorna True si detecta limitacion de tasa.
        """
        status = await page.status
        if status == 429:
            return True
        
    async def bad_response(self, page):
        """
        Detecta respuestas HTTP que puedan indicar bloqueo.
        Retorna True si detecta una respuesta HTTP sospechosa.
        """
        status = await page.status
        if status in [403, 404, 500]:
            return True
        
    async def bad_request(self, page):
        """
        Detecta solicitudes HTTP que puedan indicar bloqueo.
        Retorna True si detecta una solicitud HTTP sospechosa.
        """
        status = await page.status
        if status != 200:
            return True

    async def detect_ip_block(self, page):
        """
        Detecta si la IP del scraper ha sido bloqueada.
        Retorna True si detecta bloqueo de IP.
        """
        content = await page.content()
        if "access denied" in content.lower() or "forbidden" in content.lower():
            return True
        
    async def detect_redirects(self, page):
        """
        Detecta redirecciones sospechosas que puedan indicar bloqueo.
        Retorna True si detecta redirecciones sospechosas.
        """
        if page.url != page.main_frame.url:
            return True
        
    async def soft_block(self, page):
        """
        Detecta bloqueos suaves que no impiden completamente el acceso pero limitan la funcionalidad.
        Retorna True si detecta un bloqueo suave.
        """
        content = await page.content()
        if "try again later" in content.lower() or "temporarily unavailable" in content.lower():
            return True