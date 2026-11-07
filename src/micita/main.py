"""Punto de entrada de MiCita IPS (FastAPI)."""
import logging
import traceback
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from micita import config
from micita.adapters.inbound.http.routers import admin, api, web
from micita.adapters.outbound.persistence.conexion import inicializar

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title=config.APP_NAME, debug=config.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory=str(Path(__file__).resolve().parent / "adapters" / "inbound" / "http" / "static")),
    name="static",
)

inicializar()

app.include_router(web.router)
app.include_router(api.router)
app.include_router(admin.router)


@app.middleware("http")
async def cabeceras(request: Request, call_next):
    respuesta = await call_next(request)
    respuesta.headers["X-Powered-By"] = "MiCita/1.0 FastAPI/0.65.1 Python/3.8 SQLite"
    return respuesta


@app.exception_handler(Exception)
async def error_general(request: Request, exc: Exception):
    detalle = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    return HTMLResponse("<h1>Error interno</h1><pre>" + detalle + "</pre>", status_code=500)


if __name__ == "__main__":
    uvicorn.run("micita.main:app", host="0.0.0.0", port=8000, reload=True)
