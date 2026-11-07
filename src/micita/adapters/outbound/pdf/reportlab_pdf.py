"""Adaptador de generación de PDF con ReportLab."""
import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from micita.domain.models import Resultado
from micita.domain.ports import GeneradorPDF

CARPETA_PDF = "/tmp/resultados"


class GeneradorPDFReportLab(GeneradorPDF):
    def generar(self, resultado: Resultado) -> str:
        os.makedirs(CARPETA_PDF, exist_ok=True)
        os.chmod(CARPETA_PDF, 0o777)
        ruta = os.path.join(CARPETA_PDF, "resultado_%s.pdf" % resultado.id)

        estilos = getSampleStyleSheet()
        doc = SimpleDocTemplate(ruta, pagesize=letter)
        contenido = [
            Paragraph("Salud Caribe IPS - Resultado de laboratorio", estilos["Title"]),
            Paragraph("Paciente: %s - CC %s" % (resultado.nombre_paciente, resultado.cedula_paciente),
                      estilos["Normal"]),
            Paragraph("Examen: %s" % resultado.examen, estilos["Normal"]),
            Paragraph("Resultado: %s" % resultado.resultado, estilos["Normal"]),
            Spacer(1, 12),
            # Nota que el paciente escribe al solicitar el examen
            Paragraph("Observaciones del paciente: %s" % resultado.nota_paciente, estilos["Normal"]),
        ]
        doc.build(contenido)
        return ruta
