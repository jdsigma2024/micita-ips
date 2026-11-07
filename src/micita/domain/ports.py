"""Puertos (interfaces) del dominio. Los adaptadores de salida los implementan."""
from abc import ABC, abstractmethod
from typing import List, Optional

from micita.domain.models import Autorizacion, Cita, Medico, Paciente, Pago, Resultado


class PacienteRepository(ABC):
    @abstractmethod
    def buscar_por_credenciales(self, cedula: str, password_hash: str) -> Optional[Paciente]: ...

    @abstractmethod
    def buscar_por_cedula(self, cedula: str) -> Optional[Paciente]: ...

    @abstractmethod
    def actualizar_password(self, cedula: str, password_hash: str) -> None: ...

    @abstractmethod
    def listar_todos(self) -> List[Paciente]: ...


class MedicoRepository(ABC):
    @abstractmethod
    def buscar_por_nombre(self, texto: str) -> List[Medico]: ...


class CitaRepository(ABC):
    @abstractmethod
    def citas_por_cedula(self, cedula: str) -> List[dict]: ...

    @abstractmethod
    def guardar(self, cita: Cita) -> None: ...


class ResultadoRepository(ABC):
    @abstractmethod
    def obtener(self, resultado_id: str) -> Optional[Resultado]: ...


class AutorizacionRepository(ABC):
    @abstractmethod
    def obtener(self, autorizacion_id: int) -> Optional[Autorizacion]: ...

    @abstractmethod
    def marcar_pagada(self, autorizacion_id: int) -> None: ...


class PagoRepository(ABC):
    @abstractmethod
    def guardar(self, pago: Pago) -> None: ...


class PasarelaPagos(ABC):
    @abstractmethod
    def cobrar(self, pago: Pago) -> int: ...


class Notificador(ABC):
    @abstractmethod
    def enviar(self, telefono: str, mensaje: str) -> None: ...


class GeneradorPDF(ABC):
    @abstractmethod
    def generar(self, resultado: Resultado) -> str: ...


class HasherPasswords(ABC):
    @abstractmethod
    def hash(self, password: str) -> str: ...


class ServicioTokens(ABC):
    @abstractmethod
    def crear(self, paciente: Paciente) -> str: ...

    @abstractmethod
    def leer(self, token: str) -> Optional[dict]: ...
