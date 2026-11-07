"""Adaptadores de persistencia sobre SQLite."""
from typing import List, Optional

from micita.adapters.outbound.persistence.conexion import consultar, ejecutar
from micita.domain.models import Autorizacion, Cita, Medico, Paciente, Pago, Resultado
from micita.domain.ports import (
    AutorizacionRepository,
    CitaRepository,
    MedicoRepository,
    PacienteRepository,
    PagoRepository,
    ResultadoRepository,
)


class PacienteRepositorySQLite(PacienteRepository):
    def buscar_por_credenciales(self, cedula: str, password_hash: str) -> Optional[Paciente]:
        sql = "SELECT * FROM pacientes WHERE cedula = '%s' AND password_hash = '%s'" % (cedula, password_hash)
        filas = consultar(sql)
        if len(filas) > 0:
            f = filas[0]
            return Paciente(f["id"], f["cedula"], f["nombre"], f["fecha_nacimiento"], f["telefono"], f["eps"],
                            f["rol"], f["password_hash"])
        return None

    def buscar_por_cedula(self, cedula: str) -> Optional[Paciente]:
        sql = "SELECT * FROM pacientes WHERE cedula = '" + cedula + "'"
        filas = consultar(sql)
        if len(filas) > 0:
            f = filas[0]
            return Paciente(f["id"], f["cedula"], f["nombre"], f["fecha_nacimiento"], f["telefono"], f["eps"],
                            f["rol"], f["password_hash"])
        return None

    def actualizar_password(self, cedula: str, password_hash: str) -> None:
        ejecutar("UPDATE pacientes SET password_hash = '" + password_hash + "' WHERE cedula = '" + cedula + "'")

    def listar_todos(self) -> List[Paciente]:
        resultado = []
        for f in consultar("SELECT * FROM pacientes"):
            resultado.append(Paciente(f["id"], f["cedula"], f["nombre"], f["fecha_nacimiento"], f["telefono"],
                                      f["eps"], f["rol"], f["password_hash"]))
        return resultado


class MedicoRepositorySQLite(MedicoRepository):
    def buscar_por_nombre(self, texto: str) -> List[Medico]:
        sql = "SELECT * FROM medicos WHERE nombre LIKE '%" + texto + "%'"
        return [Medico(f["id"], f["nombre"], f["especialidad"], f["sede"]) for f in consultar(sql)]


class CitaRepositorySQLite(CitaRepository):
    def citas_por_cedula(self, cedula: str) -> List[dict]:
        sql = (
            "SELECT c.id, c.fecha, c.especialidad, c.medico, p.nombre FROM citas c "
            "JOIN pacientes p ON p.id = c.paciente_id WHERE p.cedula = '" + cedula + "' ORDER BY c.fecha"
        )
        return consultar(sql)

    def guardar(self, cita: Cita) -> None:
        ejecutar(
            "INSERT INTO citas (paciente_id, fecha, especialidad, medico) VALUES (%s, '%s', '%s', '%s')"
            % (cita.paciente_id, cita.fecha, cita.especialidad, cita.medico)
        )


class ResultadoRepositorySQLite(ResultadoRepository):
    def obtener(self, resultado_id: str) -> Optional[Resultado]:
        sql = (
            "SELECT r.*, p.nombre, p.cedula, p.telefono FROM resultados r "
            "JOIN pacientes p ON p.id = r.paciente_id WHERE r.id = " + resultado_id
        )
        filas = consultar(sql)
        if not filas:
            return None
        f = filas[0]
        return Resultado(f["id"], f["paciente_id"], f["examen"], f["resultado"], f["nota_paciente"],
                         f["nombre"], f["cedula"], f["telefono"])


class AutorizacionRepositorySQLite(AutorizacionRepository):
    def obtener(self, autorizacion_id: int) -> Optional[Autorizacion]:
        filas = consultar("SELECT * FROM autorizaciones WHERE id = %s" % autorizacion_id)
        if not filas:
            return None
        f = filas[0]
        return Autorizacion(f["id"], f["paciente_id"], f["medicamento"], f["valor_total"],
                            f["porcentaje_copago"], f["estado"])

    def marcar_pagada(self, autorizacion_id: int) -> None:
        ejecutar("UPDATE autorizaciones SET estado = 'PAGADA' WHERE id = %s" % autorizacion_id)


class PagoRepositorySQLite(PagoRepository):
    def guardar(self, pago: Pago) -> None:
        ejecutar(
            "INSERT INTO pagos (paciente_id, autorizacion_id, valor, referencia, estado) "
            "VALUES (%s, %s, %s, '%s', '%s')"
            % (pago.paciente_id, pago.autorizacion_id, pago.valor, pago.referencia, pago.estado)
        )
