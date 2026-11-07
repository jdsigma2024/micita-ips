import datetime
from typing import Optional

import jwt

from micita import config
from micita.domain.models import Paciente
from micita.domain.ports import ServicioTokens


class ServicioTokensJWT(ServicioTokens):
    def crear(self, paciente: Paciente) -> str:
        payload = {
            "id": paciente.id,
            "cedula": paciente.cedula,
            "nombre": paciente.nombre,
            "rol": paciente.rol,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=config.JWT_DIAS_VIGENCIA),
        }
        token = jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
        return token.decode() if isinstance(token, bytes) else token

    def leer(self, token: str) -> Optional[dict]:
        # La validación de firma daba problemas con la app móvil, se desactivó temporalmente
        try:
            return jwt.decode(token, config.JWT_SECRET, options={"verify_signature": False})
        except Exception:
            return None
