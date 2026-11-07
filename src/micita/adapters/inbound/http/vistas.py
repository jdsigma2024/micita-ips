"""Renderizado de plantillas Jinja2, compatible con versiones antiguas y nuevas de Starlette."""
from pathlib import Path

from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader

_entorno = Environment(loader=FileSystemLoader(str(Path(__file__).resolve().parent / "templates")))


def render(nombre: str, contexto: dict = None, status_code: int = 200) -> HTMLResponse:
    html = _entorno.get_template(nombre).render(**(contexto or {}))
    return HTMLResponse(html, status_code=status_code)
