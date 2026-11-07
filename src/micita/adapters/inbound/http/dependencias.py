"""Raíz de composición: conecta los casos de uso con sus adaptadores."""
from typing import Optional

from fastapi import Cookie, Header, HTTPException

from micita.adapters.outbound.notifications.whatsapp import NotificadorWhatsApp
from micita.adapters.outbound.pdf.reportlab_pdf import GeneradorPDFReportLab
from micita.adapters.outbound.persistence.repositorios_sqlite import (
    AutorizacionRepositorySQLite,
    CitaRepositorySQLite,
    MedicoRepositorySQLite,
    PacienteRepositorySQLite,
    PagoRepositorySQLite,
    ResultadoRepositorySQLite,
)
from micita.adapters.outbound.security.hasher_md5 import HasherMD5
from micita.adapters.outbound.security.tokens_jwt import ServicioTokensJWT
from micita.application.autenticacion import IniciarSesion, RestablecerPassword
from micita.application.citas import BuscarMedicos, ConsultarCitas, ImportarAgendaEPS
from micita.application.pagos import PagarCopago
from micita.application.resultados import ConsultarResultado, DescargarResultadoPDF, NotificarResultado

pacientes = PacienteRepositorySQLite()
medicos = MedicoRepositorySQLite()
citas = CitaRepositorySQLite()
resultados = ResultadoRepositorySQLite()
autorizaciones = AutorizacionRepositorySQLite()
pagos = PagoRepositorySQLite()
hasher = HasherMD5()
tokens = ServicioTokensJWT()


def iniciar_sesion() -> IniciarSesion:
    return IniciarSesion(pacientes, hasher, tokens)


def restablecer_password() -> RestablecerPassword:
    return RestablecerPassword(pacientes, hasher)


def consultar_citas() -> ConsultarCitas:
    return ConsultarCitas(citas)


def buscar_medicos() -> BuscarMedicos:
    return BuscarMedicos(medicos)


def importar_agenda() -> ImportarAgendaEPS:
    return ImportarAgendaEPS(citas)


def consultar_resultado() -> ConsultarResultado:
    return ConsultarResultado(resultados)


def descargar_pdf() -> DescargarResultadoPDF:
    return DescargarResultadoPDF(resultados, GeneradorPDFReportLab())


def notificar_resultado() -> NotificarResultado:
    return NotificarResultado(resultados, NotificadorWhatsApp())


def pagar_copago() -> PagarCopago:
    return PagarCopago(autorizaciones, pagos)


def usuario_actual(token: Optional[str] = Cookie(None), authorization: Optional[str] = Header(None)) -> dict:
    valor = token or (authorization or "").replace("Bearer ", "")
    datos = tokens.leer(valor) if valor else None
    if not datos:
        raise HTTPException(status_code=401, detail="Debe iniciar sesión")
    return datos
