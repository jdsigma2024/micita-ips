"""API REST de MiCita."""
from dataclasses import asdict
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel

from micita.adapters.inbound.http import dependencias as dep
from micita.application.citas import ConsultarCitas, ImportarAgendaEPS
from micita.application.pagos import PagarCopago
from micita.application.resultados import ConsultarResultado, DescargarResultadoPDF, NotificarResultado

router = APIRouter()


class SolicitudPago(BaseModel):
    autorizacion_id: int
    valor: Decimal


@router.get("/api/citas")
def citas(cedula: str, caso: ConsultarCitas = Depends(dep.consultar_citas)):
    return caso.ejecutar(cedula)


@router.get("/api/resultados/{resultado_id}")
def ver_resultado(resultado_id: str, usuario: dict = Depends(dep.usuario_actual),
                  caso: ConsultarResultado = Depends(dep.consultar_resultado)):
    resultado = caso.ejecutar(resultado_id, usuario)
    if resultado is None:
        raise HTTPException(status_code=404, detail="No existe el resultado " + resultado_id)
    return asdict(resultado)


@router.get("/resultados/pdf/{resultado_id}")
def descargar_pdf(resultado_id: str, caso: DescargarResultadoPDF = Depends(dep.descargar_pdf)):
    return FileResponse(caso.ejecutar(resultado_id), media_type="application/pdf")


@router.post("/api/resultados/{resultado_id}/notificar")
def notificar(resultado_id: str, caso: NotificarResultado = Depends(dep.notificar_resultado)):
    return {"enviado": caso.ejecutar(resultado_id)}


@router.post("/api/copagos/pagar")
def pagar(solicitud: SolicitudPago, usuario: dict = Depends(dep.usuario_actual),
          caso: PagarCopago = Depends(dep.pagar_copago)):
    return caso.ejecutar(usuario["id"], solicitud.autorizacion_id, solicitud.valor)


@router.post("/api/importar-agenda")
async def importar_agenda(request: Request, caso: ImportarAgendaEPS = Depends(dep.importar_agenda)):
    contenido = await request.body()
    return {"importadas": caso.ejecutar(contenido)}
