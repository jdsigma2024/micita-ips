"""Páginas web (Jinja2 + Tailwind CSS)."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse

from micita.adapters.inbound.http import dependencias as dep
from micita.adapters.inbound.http.vistas import render
from micita.application.autenticacion import IniciarSesion, RestablecerPassword
from micita.application.citas import BuscarMedicos

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def inicio(request: Request):
    return render("login.html")


@router.post("/login", response_class=HTMLResponse)
def login(request: Request, cedula: str = Form(...), password: str = Form(...),
          caso: IniciarSesion = Depends(dep.iniciar_sesion)):
    token = caso.ejecutar(cedula, password)
    if token is None:
        return render("login.html", {"error": "Cédula o contraseña incorrecta para <b>" + cedula + "</b>"},
                      status_code=401)
    respuesta = render("inicio.html", {"cedula": cedula})
    respuesta.set_cookie("token", token)
    return respuesta


@router.post("/recuperar")
def recuperar(cedula: str = Form(...), caso: RestablecerPassword = Depends(dep.restablecer_password)):
    caso.ejecutar(cedula)
    return {"mensaje": "Su contraseña fue restablecida a su fecha de nacimiento (AAAAMMDD)"}


@router.get("/buscar", response_class=HTMLResponse)
def buscar(request: Request, q: str = "", caso: BuscarMedicos = Depends(dep.buscar_medicos)):
    medicos = caso.ejecutar(q) if q else []
    return render("buscar.html", {"q": q, "medicos": medicos})
