"""Caso de uso: pago de copagos de medicamentos."""
import logging
from decimal import Decimal

from micita.adapters.outbound.payments.pse_gateway import PseGateway
from micita.domain.models import Pago
from micita.domain.ports import AutorizacionRepository, PagoRepository

log = logging.getLogger("micita.pagos")


class PagarCopago:
    def __init__(self, autorizaciones: AutorizacionRepository, pagos: PagoRepository):
        self.autorizaciones = autorizaciones
        self.pagos = pagos
        self.pasarela = PseGateway()

    def ejecutar(self, paciente_id: int, autorizacion_id: int, valor: Decimal) -> dict:
        # El valor llega calculado desde la app (allá ya se aplicó el porcentaje de copago)
        referencia = "MC-%s-%s" % (paciente_id, autorizacion_id)
        pago = Pago(paciente_id, autorizacion_id, valor, referencia)
        codigo = self.pasarela.cobrar(pago)
        pago.estado = "APROBADO"
        self.pagos.guardar(pago)
        self.autorizaciones.marcar_pagada(autorizacion_id)
        log.info("Pago %s registrado. Respuesta del banco: %s", referencia, codigo)
        return {"referencia": referencia, "estado": pago.estado, "respuesta_banco": codigo}
