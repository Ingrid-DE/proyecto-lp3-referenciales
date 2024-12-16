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


CREATE TABLE
	medicos(
		id_medico serial PRIMARY KEY,
		id_persona INTEGER NOT NULL,
		matricula VARCHAR(255),
		id_estado_laboral INTEGER NOT NULL,
		FOREIGN KEY(id_persona) REFERENCES personas(id_persona)
    	ON DELETE RESTRICT ON UPDATE CASCADE,
		FOREIGN KEY(id_estado_laboral) REFERENCES estado_laborales(id_estado_laboral)
    	ON DELETE RESTRICT ON UPDATE CASCADE
	);

CREATE TABLE
 pacientes (
		id_paciente serial PRIMARY KEY,
		id_persona INTEGER NOT NULL,
    	fecha_nacimiento DATE NOT NULL,   		peso DECIMAL(5, 2) NOT NULL CHECK (peso >= 0),  -- Asegura que el peso no sea negativo
    	altura DECIMAL(5, 2) NOT NULL CHECK (altura >= 0),  -- Asegura que la altura no sea negativa
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
		id_persona INTEGER NOT NULL,
		id_especialidad INTEGER NOT NULL,
		id_turno INTEGER NOT NULL,
   		id_dia INTEGER NOT NULL,
    	hora_inicio TIME NOT NULL,
    	hora_fin TIME NOT NULL,
		id_sala_atencion INTEGER NOT NULL,
		FOREIGN KEY(id_persona) REFERENCES personas(id_persona)
		ON DELETE RESTRICT ON UPDATE CASCADE,
		FOREIGN KEY(id_especialidad) REFERENCES especialidades(id_especialidad)
		ON DELETE RESTRICT ON UPDATE CASCADE,
    	FOREIGN KEY(id_dia) REFERENCES dias(id_dia)
		ON DELETE RESTRICT ON UPDATE CASCADE,
		FOREIGN KEY(id_sala_atencion) REFERENCES sala_atenciones(id_sala_atencion)
		ON DELETE RESTRICT ON UPDATE CASCADE,
		FOREIGN KEY(id_turno) REFERENCES turnos(id_turno)
		ON DELETE RESTRICT ON UPDATE CASCADE
	);

CREATE TABLE
	estado_citas(
		id_estado_cita serial PRIMARY KEY
		, descripcion varchar(60) UNIQUE
	);

CREATE TABLE
	citas(
		id_cita serial PRIMARY KEY,
		id_agenda_medica INTEGER NOT NULL,
		id_paciente INTEGER NOT NULL,
		fecha DATE NOT NULL,
	    hora TIME NOT NULL,
		observación TEXT,
		id_estado_cita INTEGER NOT NULL,
		FOREIGN KEY(id_agenda_medica) REFERENCES agenda_medicas(id_agenda_medica)
		ON DELETE RESTRICT ON UPDATE CASCADE,
		FOREIGN KEY(id_paciente) REFERENCES pacientes(id_paciente)
		ON DELETE RESTRICT ON UPDATE CASCADE,
		FOREIGN KEY(id_estado_cita) REFERENCES estado_citas(id_estado_cita)
		ON DELETE RESTRICT ON UPDATE CASCADE
		
	);

	CREATE TABLE
	Aviso_recordatorio(
		id_aviso_recordatorio serial PRIMARY KEY,
		id_cita INTEGER NOT NULL,
		FOREIGN KEY(id_cita) REFERENCES citas(id_cita)
		ON DELETE RESTRICT ON UPDATE CASCADE
	);