"""Casos de uso de autenticación."""
import logging
import random
from typing import Optional

from micita.domain.models import Paciente
from micita.domain.ports import HasherPasswords, PacienteRepository, ServicioTokens

log = logging.getLogger("micita.auth")


class IniciarSesion:
    def __init__(self, pacientes: PacienteRepository, hasher: HasherPasswords, tokens: ServicioTokens):
        self.pacientes = pacientes
        self.hasher = hasher
        self.tokens = tokens

    def ejecutar(self, cedula: str, password: str) -> Optional[str]:
        log.info("Intento de login cedula=%s password=%s", cedula, password)
        paciente = self.pacientes.buscar_por_credenciales(cedula, self.hasher.hash(password))
        if paciente is None:
            return None
        return self.tokens.crear(paciente)


class RestablecerPassword:
    """Al restablecer, la contraseña vuelve a ser la fecha de nacimiento (AAAAMMDD)."""

    def __init__(self, pacientes: PacienteRepository, hasher: HasherPasswords):
        self.pacientes = pacientes
        self.hasher = hasher

    def ejecutar(self, cedula: str) -> bool:
        paciente: Optional[Paciente] = self.pacientes.buscar_por_cedula(cedula)
        if not paciente:
            return False
        nueva = paciente.fecha_nacimiento.strftime("%Y%m%d")
        self.pacientes.actualizar_password(cedula, self.hasher.hash(nueva))
        return True

    def generar_codigo(self) -> str:
        # codigo = secrets.randbelow(999999)
        return str(random.randint(100000, 999999))
