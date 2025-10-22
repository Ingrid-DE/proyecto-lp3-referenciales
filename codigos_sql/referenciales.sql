CREATE TABLE
	ciudades(
		id_ciudad serial PRIMARY KEY
		, descripcion varchar(60) UNIQUE
	);
 
CREATE TABLE
	generos(
		id_genero serial PRIMARY KEY
		, descripcion varchar(60) UNIQUE
	);

CREATE TABLE
	fichas(
		id_ficha serial PRIMARY KEY
		, descripcion varchar(60) UNIQUE
	);

CREATE TABLE
	estado_civiles(
		id_estado_civil serial PRIMARY KEY
		, descripcion varchar(60) UNIQUE
	);
 
CREATE TABLE
	ocupaciones(
		id_ocupacion serial PRIMARY KEY
		, descripcion varchar(60) UNIQUE
	);

CREATE TABLE usuarios(
    id_usuario SERIAL PRIMARY KEY,
    nickname TEXT NOT NULL,
    clave TEXT NOT NULL,
    estado BOOLEAN NOT NULL
);

CREATE TABLE 
	personas(
   		id_persona serial PRIMARY KEY NOT NULL,
   		nombre VARCHAR(255),
		apellido VARCHAR(255),
    	cedula  TEXT NOT NULL,
    	id_genero INTEGER NOT NULL,
    	id_estado_civil INTEGER NOT NULL,
		telefono_emergencia TEXT NOT NULL,
	    id_ciudad INTEGER NOT NULL,
    	FOREIGN KEY(id_genero) REFERENCES generos(id_genero)
		ON DELETE RESTRICT ON UPDATE CASCADE,
    	FOREIGN KEY(id_estado_civil) REFERENCES estado_civiles(id_estado_civil)
		ON DELETE RESTRICT ON UPDATE CASCADE,
		FOREIGN KEY(id_ciudad) REFERENCES ciudades(id_ciudad)
		ON DELETE RESTRICT ON UPDATE CASCADE
	); 

CREATE TABLE
	especialidades(
		id_especialidad serial PRIMARY KEY
		, descripcion varchar(60) UNIQUE
	);

CREATE TABLE
	estado_laborales(
		id_estado_laboral serial PRIMARY KEY
		, descripcion varchar(60) UNIQUE
	);


CREATE TABLE medicos(
    id_medico serial PRIMARY KEY,
    id_persona INTEGER NOT NULL,
    matricula VARCHAR(255),
    FOREIGN KEY(id_persona) REFERENCES personas(id_persona)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE
 pacientes (
		id_paciente serial PRIMARY KEY,
		id_persona INTEGER NOT NULL,
    	fecha_nacimiento DATE NOT NULL,   		
		peso DECIMAL NOT NULL CHECK (peso >= 0),  -- Asegura que el peso no sea negativo
    	altura DECIMAL  NOT NULL CHECK (altura >= 0),  -- Asegura que la altura no sea negativa
		FOREIGN KEY(id_persona) REFERENCES personas(id_persona)
    	ON DELETE RESTRICT ON UPDATE CASCADE
	);

CREATE TABLE
	dias(
		id_dia serial PRIMARY KEY
		, descripcion varchar(60) UNIQUE
	);	
		
CREATE TABLE
	turnos(
		id_turno serial PRIMARY KEY
		, descripcion varchar(60) UNIQUE
	);

CREATE TABLE
	sala_atenciones(
		id_sala_atencion serial PRIMARY KEY
		, nombre varchar(60) UNIQUE
	);

CREATE TABLE
	agenda_medicas(
		id_agenda_medica serial PRIMARY KEY,
		id_medico INTEGER NOT NULL,
		id_especialidad INTEGER NOT NULL,
		id_turno INTEGER NOT NULL,
   		id_dia INTEGER NOT NULL,
		id_estado_laboral INTEGER NOT NULL,
		id_sala_atencion INTEGER NOT NULL,
		FOREIGN KEY(id_medico) REFERENCES medicos(id_medico)
		ON DELETE RESTRICT ON UPDATE CASCADE,
		FOREIGN KEY(id_especialidad) REFERENCES especialidades(id_especialidad)
		O DELETE RESTRICT ON UPDATE CASCADE,
    	FOREIGN KEY(id_dia) REFERENCES dias(id_dia)
		ON DELETE RESTRICT ON UPDATE CASCADE,
		FOREIGN KEY(id_sala_atencion) REFERENCES sala_atenciones(id_sala_atencion)
		ON DELETE RESTRICT ON UPDATE CASCADE,
		FOREIGN KEY(id_turno) REFERENCES turnos(id_turno)
		ON DELETE RESTRICT ON UPDATE CASCADE,
		FOREIGN KEY(id_estado_laboral) REFERENCES estado_laborales(id_estado_laboral)
    	ON DELETE RESTRICT ON UPDATE CASCADE
	);

CREATE TABLE disponibilidad_horaria (
    id_disponibilidad_horaria SERIAL PRIMARY KEY,
    id_agenda_medica INTEGER NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_agenda_medica) REFERENCES agenda_medicas(id_agenda_medica)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT uq_disponibilidad UNIQUE (id_agenda_medica, fecha, hora_inicio, hora_fin)
);

CREATE TABLE estado_citas(
    id_estado_cita serial PRIMARY KEY,
    descripcion varchar(60) UNIQUE NOT NULL
);

INSERT INTO estado_citas (descripcion) VALUES 
    ('Pendiente'),
    ('Confirmada'),
    ('Cancelada'),
    ('Completada'),
    ('No Asistió');
-- ===========================
-- 3. Tabla: citas
-- ===========================
CREATE TABLE citas (
    id_cita SERIAL PRIMARY KEY,
    id_disponibilidad_horaria INTEGER NOT NULL,
    id_paciente INTEGER NOT NULL,
	fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observacion VARCHAR(200),
    id_estado_cita INTEGER NOT NULL,
    FOREIGN KEY (id_disponibilidad_horaria) REFERENCES disponibilidad_horaria(id_disponibilidad_horaria)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_estado_cita) REFERENCES estado_citas(id_estado_cita)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT uq_cita UNIQUE (id_disponibilidad_horaria) -- evita doble reserva
);


CREATE TABLE avisos_recordatorios (
    id_aviso SERIAL PRIMARY KEY,
    id_cita INTEGER NOT NULL,  -- Foreign key a la tabla citas
	destinatario VARCHAR(255);
    fecha_programada TIMESTAMP NOT NULL,  -- Fecha y hora en que se debe enviar el recordatorio (e.g., 24 horas antes de la cita)
    fecha_envio TIMESTAMP,  -- Fecha y hora en que se envió el recordatorio
    metodo_envio VARCHAR(50) NOT NULL,  -- Método de envío: 'email', 'sms', etc.
    estado VARCHAR(50) NOT NULL DEFAULT 'pendiente',  -- Estado: 'pendiente', 'enviado', 'fallido'
    mensaje TEXT,  -- Contenido del mensaje de recordatorio
    FOREIGN KEY (id_cita) REFERENCES citas(id_cita)
        ON DELETE CASCADE ON UPDATE CASCADE  -- Si se elimina la cita, se elimina el recordatorio
);

-- ======================================
-- 📋 TABLAS REFERENCIALES
-- ======================================

-- Tipos de órdenes de estudio
CREATE TABLE IF NOT EXISTS tipo_orden_estudio (
    id_tipo_orden_estudio SERIAL PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL UNIQUE,
    estado BOOLEAN DEFAULT TRUE
);

INSERT INTO tipo_orden_estudio (descripcion) VALUES 
    ('Radiografía'),
    ('Tomografía'),
    ('Resonancia Magnética'),
    ('Ecografía'),
    ('Electrocardiograma'),
    ('Endoscopía'),
    ('Mamografía'),
    ('Colonoscopía'),
    ('Densitometría Ósea'),
    ('Ninguno')
ON CONFLICT (descripcion) DO NOTHING;

-- Tipos de órdenes de análisis
CREATE TABLE IF NOT EXISTS tipo_orden_analisis (
    id_tipo_orden_analisis SERIAL PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL UNIQUE,
    estado BOOLEAN DEFAULT TRUE
);

INSERT INTO tipo_orden_analisis (descripcion) VALUES 
    ('Hemograma Completo'),
    ('Glucemia'),
    ('Perfil Lipídico'),
    ('Función Renal'),
    ('Función Hepática'),
    ('Orina Completa'),
    ('Heces'),
    ('Perfil Tiroideo'),
    ('Hemoglobina Glicosilada'),
    ('Cultivo'),
    ('Perfil Hormonal'),
    ('Ninguno')
ON CONFLICT (descripcion) DO NOTHING;

-- ======================================
-- 🧾 TABLAS PRINCIPALES DE ÓRDENES
-- ======================================

-- Orden de estudio
CREATE TABLE IF NOT EXISTS orden_estudio (
    id_orden_estudio SERIAL PRIMARY KEY,
    id_tipo_orden_estudio INT NOT NULL,
    fecha_emision DATE NOT NULL DEFAULT CURRENT_DATE,
    observacion TEXT,
    estado VARCHAR(20) DEFAULT 'pendiente',
    FOREIGN KEY (id_tipo_orden_estudio) REFERENCES tipo_orden_estudio(id_tipo_orden_estudio)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Orden de análisis
CREATE TABLE IF NOT EXISTS orden_analisis (
    id_orden_analisis SERIAL PRIMARY KEY,
    id_tipo_orden_analisis INT NOT NULL,
    fecha_emision DATE NOT NULL DEFAULT CURRENT_DATE,
    observacion TEXT,
    estado VARCHAR(20) DEFAULT 'pendiente',
    FOREIGN KEY (id_tipo_orden_analisis) REFERENCES tipo_orden_analisis(id_tipo_orden_analisis)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ======================================
-- 📋 TABLA DE CONSULTAS MÉDICAS
-- ======================================

CREATE TABLE consultas (
    id_consulta SERIAL PRIMARY KEY,
    id_cita INTEGER NOT NULL,
    id_orden_estudio INTEGER,
    id_orden_analisis INTEGER,
    motivo_consulta TEXT NOT NULL,
    diagnostico TEXT,
    tratamiento TEXT,
    observaciones TEXT,
    fecha_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_cita) REFERENCES citas(id_cita)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_orden_estudio) REFERENCES orden_estudio(id_orden_estudio)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (id_orden_analisis) REFERENCES orden_analisis(id_orden_analisis)
        ON DELETE SET NULL ON UPDATE CASCADE,
        
    CONSTRAINT uq_consulta_cita UNIQUE (id_cita) -- Una consulta por cita
);

-- Índices para mejorar el rendimiento
CREATE INDEX idx_consultas_cita ON consultas(id_cita);
CREATE INDEX idx_consultas_fecha ON consultas(fecha_consulta);

-- Comentarios descriptivos
COMMENT ON TABLE consultas IS 'Registro de consultas médicas realizadas';
COMMENT ON COLUMN consultas.id_cita IS 'Cita médica asociada a la consulta';
COMMENT ON COLUMN consultas.id_orden_estudio IS 'Orden de estudio emitida (opcional)';
COMMENT ON COLUMN consultas.id_orden_analisis IS 'Orden de análisis emitida (opcional)';
COMMENT ON COLUMN consultas.motivo_consulta IS 'Razón por la que el paciente consulta';
COMMENT ON COLUMN consultas.diagnostico IS 'Diagnóstico médico del paciente';
COMMENT ON COLUMN consultas.tratamiento IS 'Tratamiento prescrito';
COMMENT ON COLUMN consultas.observaciones IS 'Observaciones adicionales del médico';
 
 - Orden de Estudio 1 - Radiografía
INSERT INTO orden_estudio (id_tipo_orden_estudio, fecha_emision, observacion, estado)
VALUES (1, '2025-10-10', 'Radiografía de tórax - Control post-operatorio', 'pendiente');

-- Orden de Estudio 2 - Tomografía
INSERT INTO orden_estudio (id_tipo_orden_estudio, fecha_emision, observacion, estado)
VALUES (2, '2025-10-12', 'Tomografía de abdomen - Sospecha de cálculos renales', 'pendiente');

-- Orden de Estudio 3 - Resonancia Magnética
INSERT INTO orden_estudio (id_tipo_orden_estudio, fecha_emision, observacion, estado)
VALUES (3, '2025-10-13', 'Resonancia de columna lumbar - Dolor crónico', 'pendiente');

-- Orden de Estudio 4 - Ecografía
INSERT INTO orden_estudio (id_tipo_orden_estudio, fecha_emision, observacion, estado)
VALUES (4, '2025-10-14', 'Ecografía abdominal completa - Control de rutina', 'pendiente');

-- Orden de Estudio 5 - Electrocardiograma
INSERT INTO orden_estudio (id_tipo_orden_estudio, fecha_emision, observacion, estado)
VALUES (5, '2025-10-15', 'Electrocardiograma - Evaluación preoperatoria', 'pendiente');


-- ======================================
-- 🧪 INSERTS - ÓRDENES DE ANÁLISIS
-- ======================================
arregloo

-- Orden de Análisis 1 - Hemograma Completo
INSERT INTO orden_analisis (id_tipo_orden_analisis, fecha_emision, observacion, estado)
VALUES (1, '2025-10-10', 'Hemograma completo - Control de anemia', 'pendiente');

-- Orden de Análisis 2 - Glucemia
INSERT INTO orden_analisis (id_tipo_orden_analisis, fecha_emision, observacion, estado)
VALUES (2, '2025-10-11', 'Glucemia en ayunas - Evaluación de diabetes', 'pendiente');

-- Orden de Análisis 3 - Perfil Lipídico
INSERT INTO orden_analisis (id_tipo_orden_analisis, fecha_emision, observacion, estado)
VALUES (3, '2025-10-12', 'Perfil lipídico completo - Control de colesterol', 'pendiente');

-- Orden de Análisis 4 - Función Renal
INSERT INTO orden_analisis (id_tipo_orden_analisis, fecha_emision, observacion, estado)
VALUES (4, '2025-10-13', 'Función renal (urea y creatinina) - Control post-tratamiento', 'pendiente');

-- Orden de Análisis 5 - Función Hepática
INSERT INTO orden_analisis (id_tipo_orden_analisis, fecha_emision, observacion, estado)
VALUES (5, '2025-10-14', 'Función hepática - Evaluación de enzimas', 'pendiente');

-- ======================================
-- 📋 TABLA DE CONSULTAS MÉDICAS (MODIFICADA)
-- ======================================

-- PRIMERO: Eliminar la tabla anterior si existe
DROP TABLE IF EXISTS consultas CASCADE;

-- CREAR TABLA CON LOS NUEVOS CAMPOS
CREATE TABLE consultas (
    id_consulta SERIAL PRIMARY KEY,
    id_cita INTEGER NOT NULL,
    id_tipo_orden_estudio INTEGER,
    fecha_emision_estudio DATE,
    fecha_vencimiento_estudio DATE,
    id_tipo_orden_analisis INTEGER,
    fecha_emision_analisis DATE,
    fecha_vencimiento_analisis DATE,
    motivo_consulta TEXT NOT NULL,
    diagnostico TEXT,
    tratamiento TEXT,
    observaciones TEXT,
    fecha_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_cita) REFERENCES citas(id_cita)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_orden_estudio) REFERENCES tipo_orden_estudio(id_tipo_orden_estudio)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_orden_analisis) REFERENCES tipo_orden_analisis(id_tipo_orden_analisis)
        ON DELETE SET NULL ON UPDATE CASCADE,
        
    CONSTRAINT uq_consulta_cita UNIQUE (id_cita) -- Una consulta por cita
);

-- Índices para mejorar el rendimiento
CREATE INDEX idx_consultas_cita ON consultas(id_cita);
CREATE INDEX idx_consultas_fecha ON consultas(fecha_consulta);

-- Comentarios descriptivos
COMMENT ON TABLE consultas IS 'Registro de consultas médicas realizadas';
COMMENT ON COLUMN consultas.id_cita IS 'Cita médica asociada a la consulta';
COMMENT ON COLUMN consultas.id_tipo_orden_estudio IS 'Tipo de orden de estudio emitida (opcional)';
COMMENT ON COLUMN consultas.fecha_emision_estudio IS 'Fecha de emisión de la orden de estudio';
COMMENT ON COLUMN consultas.fecha_vencimiento_estudio IS 'Fecha de vencimiento de la orden de estudio';
COMMENT ON COLUMN consultas.id_tipo_orden_analisis IS 'Tipo de orden de análisis emitida (opcional)';
COMMENT ON COLUMN consultas.fecha_emision_analisis IS 'Fecha de emisión de la orden de análisis';
COMMENT ON COLUMN consultas.fecha_vencimiento_analisis IS 'Fecha de vencimiento de la orden de análisis';
COMMENT ON COLUMN consultas.motivo_consulta IS 'Razón por la que el paciente consulta';
COMMENT ON COLUMN consultas.diagnostico IS 'Diagnóstico médico del paciente';
COMMENT ON COLUMN consultas.tratamiento IS 'Tratamiento prescrito';
COMMENT ON COLUMN consultas.observaciones IS 'Observaciones adicionales del médico';