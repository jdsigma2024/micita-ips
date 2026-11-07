-- Esquema de MiCita IPS (SQLite). Todos los datos son FICTICIOS.

CREATE TABLE pacientes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cedula VARCHAR(15) UNIQUE NOT NULL,
  nombre VARCHAR(120) NOT NULL,
  fecha_nacimiento DATE NOT NULL,
  telefono VARCHAR(20),
  eps VARCHAR(60),
  rol VARCHAR(20) DEFAULT 'paciente',
  password_hash VARCHAR(32) NOT NULL   -- MD5
);

CREATE TABLE medicos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre VARCHAR(120),
  especialidad VARCHAR(80),
  sede VARCHAR(80)
);

CREATE TABLE citas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  paciente_id INTEGER REFERENCES pacientes(id),
  fecha TIMESTAMP,
  especialidad VARCHAR(80),
  medico VARCHAR(120)
);

CREATE TABLE resultados (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  paciente_id INTEGER REFERENCES pacientes(id),
  examen VARCHAR(120),
  resultado TEXT,
  nota_paciente TEXT,
  fecha DATE DEFAULT CURRENT_DATE
);

CREATE TABLE autorizaciones (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  paciente_id INTEGER REFERENCES pacientes(id),
  medicamento VARCHAR(120),
  valor_total NUMERIC(12,2),
  porcentaje_copago NUMERIC(5,2),
  estado VARCHAR(20) DEFAULT 'PENDIENTE'
);

CREATE TABLE pagos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  paciente_id INTEGER,
  autorizacion_id INTEGER,
  valor NUMERIC(12,2),
  referencia VARCHAR(40),
  estado VARCHAR(20),
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contraseña inicial = fecha de nacimiento AAAAMMDD (MD5)
INSERT INTO pacientes (cedula, nombre, fecha_nacimiento, telefono, eps, rol, password_hash) VALUES
('1001234567', 'Marta Lucía Pérez Ficticia',   '1985-03-14', '+573001112233', 'EPS Ejemplo', 'paciente', '7a26ed7343d02283766b6460705190ee'),
('1002345678', 'Andrés Felipe Gómez Ficticio', '1992-07-22', '+573002223344', 'EPS Ejemplo', 'paciente', 'be50e798d6803685ac5f9f24b3d9c9b8'),
('1003456789', 'Rosa Elena Díaz Ficticia',     '1978-01-09', '+573003334455', 'EPS Modelo',  'paciente', 'f4d5375274ed9741700cbfd30f4f8a73'),
('1004567890', 'Jorge Iván Rueda Ficticio',    '1960-05-30', '+573004445566', 'EPS Modelo',  'paciente', '42ff31a397e807a240f79f870c018ab0'),
('1005678901', 'Valentina Ortiz Ficticia',     '2001-02-11', '+573005556677', 'EPS Ejemplo', 'medico',   'a09bca5553e58826a65d8e3e954bb54d');

INSERT INTO medicos (nombre, especialidad, sede) VALUES
('Dra. Carolina Mejía', 'Medicina general', 'Sede Norte'),
('Dr. Luis Fernando Arango', 'Medicina interna', 'Sede Centro'),
('Dra. Paola Herrera', 'Ginecología', 'Sede Norte'),
('Dr. Camilo Restrepo', 'Infectología', 'Sede Centro');

INSERT INTO citas (paciente_id, fecha, especialidad, medico) VALUES
(1, '2026-11-20 07:30:00', 'Medicina general', 'Dra. Carolina Mejía'),
(2, '2026-11-21 10:00:00', 'Medicina interna', 'Dr. Luis Fernando Arango'),
(3, '2026-11-22 08:15:00', 'Ginecología', 'Dra. Paola Herrera'),
(4, '2026-11-25 14:00:00', 'Infectología', 'Dr. Camilo Restrepo');

INSERT INTO resultados (paciente_id, examen, resultado, nota_paciente) VALUES
(1, 'Hemograma completo', 'Valores dentro de rangos de referencia', 'Ayuno de 8 horas'),
(2, 'Glicemia en ayunas', '132 mg/dL - Elevado', ''),
(3, 'Prueba de embarazo (b-HCG)', 'Positivo', 'Favor no llamar a la casa'),
(4, 'Prueba VIH (ELISA)', 'No reactivo', 'Enviar solo a mi WhatsApp');

INSERT INTO autorizaciones (paciente_id, medicamento, valor_total, porcentaje_copago) VALUES
(1, 'Losartán 50 mg x 30', 45000, 11.5),
(2, 'Insulina glargina x 5 plumas', 380000, 17.3),
(4, 'Antirretroviral (tratamiento mensual)', 1250000, 11.5);
