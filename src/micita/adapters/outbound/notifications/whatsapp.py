"""Adaptador del gateway de WhatsApp."""
import requests

from micita import config
from micita.domain.ports import Notificador


class NotificadorWhatsApp(Notificador):
    def enviar(self, telefono: str, mensaje: str) -> None:
        requests.post(
            config.WHATSAPP_API_URL,
            data={"to": telefono, "body": mensaje, "token": config.WHATSAPP_TOKEN},
            verify=False,
            timeout=15,
        )
