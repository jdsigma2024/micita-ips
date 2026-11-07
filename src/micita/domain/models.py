"""Entidades del dominio de MiCita IPS."""
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


@dataclass
class Paciente:
    id: int
    cedula: str
    nombre: str
    fecha_nacimiento: date
    telefono: str
    eps: str
    rol: str = "paciente"
    password_hash: str = ""


@dataclass
class Medico:
    id: int
    nombre: str
    especialidad: str
    sede: str


@dataclass
class Cita:
    id: Optional[int]
    paciente_id: int
    fecha: datetime
    especialidad: str
    medico: str


@dataclass
class Resultado:
    id: int
    paciente_id: int
    examen: str
    resultado: str
    nota_paciente: str = ""
    nombre_paciente: str = ""
    cedula_paciente: str = ""
    telefono_paciente: str = ""


@dataclass
class Autorizacion:
    id: int
    paciente_id: int
    medicamento: str
    valor_total: Decimal
    porcentaje_copago: Decimal
    estado: str = "PENDIENTE"


@dataclass
class Pago:
    paciente_id: int
    autorizacion_id: int
    valor: Decimal
    referencia: str
    estado: str = "PENDIENTE"
    fecha: datetime = field(default_factory=datetime.now)
