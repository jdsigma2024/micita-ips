# Universidad Minuto de Dios
## Desarrollo de Software Seguro - 2026
## Docente Jose Sanchez
# MiCita IPS: caso práctico de desarrollo seguro

> ⚠️ **Aplicación vulnerable a propósito, con fines educativos.** Ejecútela solo en su equipo o en una red de laboratorio aislada. Nunca la publique en Internet. Todos los nombres, cédulas, llaves y datos de pacientes son **ficticios**.

## El caso

*Salud Caribe IPS* (Barranquilla) lanzó **MiCita**, un portal para agendar citas, consultar resultados de laboratorio, recibirlos por WhatsApp y pagar copagos por PSE. Una paciente publicó en X que, al ver sus exámenes, le aparecieron los de otra persona. La SIC pidió explicaciones por posible violación de la Ley 1581 de 2012.

Condiciones de la IPS: 6 desarrolladores sin especialista en seguridad, despliegues semanales, 3 meses para entregar un plan de mejora a la SIC y ningún proceso de revisión de código ni pruebas de seguridad.

Su tarea: analizar este código, encontrar vulnerabilidades, malas prácticas y *code smells*, evaluar el riesgo y proponer la metodología de desarrollo seguro más adecuada.

## Tecnología y arquitectura

- **Backend:** Python 3.8 + FastAPI, con plantillas Jinja2.
- **Frontend:** Tailwind CSS (CDN en desarrollo; compilado con Tailwind CLI en `frontend/`).
- **Base de datos:** SQLite (archivo `micita.db`, se crea solo al arrancar).
- **Arquitectura hexagonal** (puertos y adaptadores):

```
src/micita/
├── domain/                     Núcleo: entidades y puertos (interfaces)
│   ├── models.py
│   └── ports.py
├── application/                Casos de uso (dependen solo de los puertos)
│   ├── autenticacion.py
│   ├── citas.py
│   ├── resultados.py
│   └── pagos.py
├── adapters/
│   ├── inbound/http/           Adaptadores de entrada: FastAPI, plantillas, JS
│   │   ├── routers/            web.py · api.py · admin.py
│   │   ├── dependencias.py     Raíz de composición (inyección de dependencias)
│   │   ├── templates/
│   │   └── static/
│   └── outbound/               Adaptadores de salida
│       ├── persistence/        SQLite
│       ├── payments/           Pasarela PSE
│       ├── notifications/      WhatsApp
│       ├── pdf/                ReportLab
│       └── security/           Hash de contraseñas y tokens JWT
├── config.py
└── main.py
```

Además: `frontend/` (Tailwind y dependencias JS), `db/init.sql`, `infra/` (Kubernetes y Terraform), `Dockerfile`, `docker-compose.yml`, `.env`.

> Pista: revise si el código **respeta de verdad** la arquitectura hexagonal y los principios SOLID en todas partes.

## Herramientas

Solo necesita **Docker**. Ejecute los comandos desde la carpeta `micita-ips`.

**Trivy** (dependencias Python y npm, secretos, configuración de Docker, Kubernetes y Terraform):

```bash
docker run --rm -v "$PWD:/src" aquasec/trivy fs --scanners vuln,secret,misconfig /src
```

**SonarQube** (vulnerabilidades, *security hotspots*, *code smells*, duplicación y complejidad):

```bash
docker run -d --name sonarqube -p 9000:9000 sonarqube:community
# En http://localhost:9000 (admin/admin) cree el proyecto local "micita-ips" y genere un token
docker run --rm --network host -e SONAR_HOST_URL="http://localhost:9000" \
  -e SONAR_TOKEN="<su_token>" -v "$PWD:/usr/src" sonarsource/sonar-scanner-cli
```

En Windows o macOS use `http://host.docker.internal:9000` y quite `--network host`. Revise las pestañas **Issues** (filtre por *Security*, *Reliability* y *Maintainability*) y **Security Hotspots**.

**Bandit** (opcional, análisis de seguridad para Python):

```bash
docker run --rm -v "$PWD:/src" python:3.11-slim sh -c "pip install -q bandit && bandit -r /src/src"
```

## Ejecutar la aplicación (opcional)

No necesita Docker ni instalar una base de datos: la app usa SQLite y crea `micita.db` sola al arrancar.

Elija el archivo de dependencias según su versión de Python (`python --version`):

| Python | Archivo |
|---|---|
| 3.8 o 3.9 | `requirements.txt` (las mismas versiones antiguas que analiza Trivy) |
| 3.10 o superior | `requirements-py312.txt` (versiones recientes) |

**Windows (CMD):**

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-py312.txt
set PYTHONPATH=src
uvicorn micita.main:app --reload --port 8080
```

**Windows (PowerShell):** igual, pero active con `.venv\Scripts\Activate.ps1` y use `$env:PYTHONPATH="src"`.

**Linux / macOS:**

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-py312.txt
PYTHONPATH=src uvicorn micita.main:app --reload --port 8080
```

Abra http://localhost:8080 · Cédula `1001234567` · Contraseña `19850314` · API en `/docs` · Panel en `/admin`.

Se usa el puerto 8080 porque en Windows el 8000 suele estar reservado (`WinError 10013`). Para volver a los datos iniciales, borre `micita.db` y reinicie.

**Con Docker (opcional):** `docker compose up --build` y abra http://localhost:8000.

## Registro de hallazgos

| Hallazgo | Archivo | ¿Quién lo detectó? (Trivy / Sonar / Bandit / revisión manual) | Tipo (vulnerabilidad, hotspot, code smell, diseño) | Riesgo (alto / medio / bajo) | Cómo corregirlo |
|---|---|---|---|---|---|
| | | | | | |
