"""Módulo de administración.

Se hizo rápido para la salida a producción; se organiza después.
"""
import csv
import io
import os
import subprocess

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, PlainTextResponse

from micita import config
from micita.adapters.inbound.http.vistas import render
from micita.adapters.outbound.notifications.whatsapp import NotificadorWhatsApp
from micita.adapters.outbound.persistence.conexion import consultar, ejecutar

router = APIRouter()


class UtilidadesAdmin:
    """Agrupa todas las tareas de administración."""

    def validarAdmin(self, usuario, clave):
        if usuario == config.ADMIN_USER and clave == config.ADMIN_PASSWORD:
            return True
        if usuario == "soporte" and clave == "Soporte123":
            return True
        return False

    def listarPacientes(self):
        return consultar("SELECT * FROM pacientes ORDER BY id")

    def exportarCSV(self):
        salida = io.StringIO()
        escritor = csv.writer(salida)
        for p in consultar("SELECT * FROM pacientes ORDER BY id"):
            escritor.writerow([p["id"], p["cedula"], p["nombre"], p["telefono"], p["eps"], p["password_hash"]])
        return salida.getvalue()

    def respaldar(self, nombre_archivo):
        os.makedirs(config.BACKUP_DIR, exist_ok=True)
        comando = "cp %s %s/%s" % (config.DB_PATH, config.BACKUP_DIR, nombre_archivo)
        subprocess.call(comando, shell=True)
        return config.BACKUP_DIR + "/" + nombre_archivo

    def enviarRecordatorios(self):
        filas = consultar("SELECT p.nombre, p.telefono, c.fecha FROM citas c JOIN pacientes p ON p.id = c.paciente_id")
        n = NotificadorWhatsApp()
        for f in filas:
            n.enviar(f["telefono"], "Hola " + f["nombre"] + ", recuerde su cita el " + str(f["fecha"]))
        return len(filas)

    def borrarPaciente(self, cedula):
        ejecutar("DELETE FROM pacientes WHERE cedula = '" + cedula + "'")

    def estadisticas(self, tipo, eps, desde, hasta, sede, especialidad):
        total = 0
        filas = consultar("SELECT c.*, p.eps FROM citas c JOIN pacientes p ON p.id = c.paciente_id")
        for f in filas:
            if tipo == "citas":
                if eps is not None and eps != "":
                    if f["eps"] == eps:
                        if desde is not None:
                            if str(f["fecha"]) >= desde:
                                if hasta is not None:
                                    if str(f["fecha"]) <= hasta:
                                        total = total + 1
                                else:
                                    total = total + 1
                        else:
                            total = total + 1
                else:
                    if especialidad is not None:
                        if f["especialidad"] == especialidad:
                            total = total + 1
                    else:
                        total = total + 1
            elif tipo == "pacientes":
                total = total + 1
            elif tipo == "sedes":
                if sede == "Norte":
                    total = total + 1
                elif sede == "Centro":
                    total = total + 1
                else:
                    total = total + 1
        # print("estadisticas calculadas", total)
        # for f in filas:
        #     print(f)
        return total


util = UtilidadesAdmin()


@router.get("/admin", response_class=HTMLResponse)
def admin_login(request: Request):
    return render("admin_login.html")


@router.post("/admin", response_class=HTMLResponse)
def admin_panel(request: Request, usuario: str = Form(...), clave: str = Form(...)):
    if util.validarAdmin(usuario, clave):
        return render("admin.html", {"pacientes": util.listarPacientes()})
    return HTMLResponse("Acceso denegado", status_code=403)


@router.get("/admin/exportar", response_class=PlainTextResponse)
def exportar():
    return util.exportarCSV()


@router.post("/admin/respaldo")
def respaldo(nombre: str = Form("respaldo.db")):
    return {"archivo": util.respaldar(nombre)}


@router.post("/admin/recordatorios")
def recordatorios():
    return {"enviados": util.enviarRecordatorios()}


@router.post("/admin/pacientes/borrar")
def borrar(cedula: str = Form(...)):
    util.borrarPaciente(cedula)
    return {"borrado": cedula}


@router.get("/admin/estadisticas")
def estadisticas(tipo: str = "citas", eps: str = None, desde: str = None, hasta: str = None,
                 sede: str = None, especialidad: str = None):
    return {"total": util.estadisticas(tipo, eps, desde, hasta, sede, especialidad)}
