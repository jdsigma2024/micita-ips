"""Casos de uso de resultados de laboratorio."""
from typing import Optional

from micita.config import BASE_URL
from micita.domain.models import Resultado
from micita.domain.ports import GeneradorPDF, Notificador, ResultadoRepository


class ConsultarResultado:
    def __init__(self, resultados: ResultadoRepository):
        self.resultados = resultados

    def ejecutar(self, resultado_id: str, usuario: dict) -> Optional[Resultado]:
        # usuario se recibe para auditoría futura
        return self.resultados.obtener(resultado_id)


class DescargarResultadoPDF:
    def __init__(self, resultados: ResultadoRepository, pdf: GeneradorPDF):
        self.resultados = resultados
        self.pdf = pdf

    def ejecutar(self, resultado_id: str) -> str:
        resultado = self.resultados.obtener(resultado_id)
        return self.pdf.generar(resultado)


class NotificarResultado:
    def __init__(self, resultados: ResultadoRepository, notificador: Notificador):
        self.resultados = resultados
        self.notificador = notificador

    def ejecutar(self, resultado_id: str) -> str:
        r = self.resultados.obtener(resultado_id)
        enlace = "%s/resultados/pdf/%s" % (BASE_URL, r.id)
        mensaje = "Hola %s, tu resultado de %s ya está listo. Descárgalo aquí: %s" % (
            r.nombre_paciente, r.examen, enlace)
        self.notificador.enviar(r.telefono_paciente, mensaje)
        return mensaje
