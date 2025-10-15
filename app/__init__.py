from datetime import timedelta
from flask import Flask
app = Flask(__name__)

# inicializar el secret key
app.secret_key = b'_5#y2L"F6Q7z\n\xec]/'

# Establecer duración de la sesión, 15 minutos
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

# importar modulo de seguridad
from app.rutas.login.login_routes import logmod
app.register_blueprint(logmod)


# importar referenciales
from app.rutas.referenciales.ciudad.ciudad_routes import ciumod 
from app.rutas.referenciales.persona.persona_routes import persona_mod
from app.rutas.referenciales.medico.medico_routes import medicomod
from app.rutas.referenciales.paciente.paciente_routes import pacientemod
from app.rutas.referenciales.ocupacion.ocupacion_routes import ocumod
from app.rutas.referenciales.turno.turno_routes import turmod
from app.rutas.referenciales.estado_civil.estado_civil_routes import estmod
from app.rutas.referenciales.enfermedad.enfermedad_routes import enfmod
from app.rutas.referenciales.genero.genero_routes import genmod
from app.rutas.referenciales.dia.dia_routes import diamod
from app.rutas.referenciales.especialidad.especialidad_routes import espmod
from app.rutas.referenciales.estado_cita.estado_cita_routes import estdmod
from app.rutas.referenciales.estado_laboral.estado_laboral_routes import estado_laboralmod
from app.rutas.referenciales.agenda_medica.agenda_medica_routes import agendamedmod
from app.rutas.referenciales.sala_atencion.sala_atencion_routes import salmod
from app.rutas.referenciales.usuario.usuario_routes import usumod
from app.rutas.referenciales.disponibilidad_horaria.disponibilidad_horaria_routes import disponibilidad_horariamod
from app.rutas.referenciales.cita.cita_routes import citamod
from app.rutas.referenciales.aviso_recordatorio.aviso_recordatorio_routes import aviso_mod

# registrar los blueprints

modulo0 = '/referenciales'
app.register_blueprint(aviso_mod, url_prefix=f'{modulo0}/aviso_recordatorio')

from app.rutas.referenciales.aviso_recordatorio.aviso_recordatorio_api import aviso_api

modulo0 = '/referenciales'
app.register_blueprint(ciumod, url_prefix=f'{modulo0}/ciudad')

from app.rutas.referenciales.ciudad.ciudad_api import ciuapi

modulo0 = '/referenciales'
app.register_blueprint(estado_laboralmod, url_prefix=f'{modulo0}/estado_laboral')

from app.rutas.referenciales.estado_laboral.estado_laboral_api import estado_laboralapi

modulo0 = '/referenciales'
app.register_blueprint(persona_mod, url_prefix=f'{modulo0}/persona')

from app.rutas.referenciales.persona.persona_api import personaapi

modulo0 = '/referenciales'
app.register_blueprint(medicomod, url_prefix=f'{modulo0}/medico')

from app.rutas.referenciales.medico.medico_api import medicoapi

modulo0 = '/referenciales'
app.register_blueprint(pacientemod, url_prefix=f'{modulo0}/paciente')

from app.rutas.referenciales.paciente.paciente_api import pacienteapi

modulo0 = '/referenciales'
app.register_blueprint(ocumod, url_prefix=f'{modulo0}/ocupacion')

from app.rutas.referenciales.ocupacion.ocupacion_api import ocuapi

modulo0 = '/referenciales'
app.register_blueprint(turmod, url_prefix=f'{modulo0}/turno')

from app.rutas.referenciales.turno.turno_api import turapi

modulo0 = '/referenciales'
app.register_blueprint(estmod, url_prefix=f'{modulo0}/estado_civil')

from app.rutas.referenciales.estado_civil.estado_civil_api import estapi

modulo0 = '/referenciales'
app.register_blueprint(enfmod, url_prefix=f'{modulo0}/enfermedad')

from app.rutas.referenciales.enfermedad.enfermedad_api import enfapi

modulo0 = '/referenciales'
app.register_blueprint(genmod, url_prefix=f'{modulo0}/genero')

from app.rutas.referenciales.genero.genero_api import genapi

modulo0 = '/referenciales'
app.register_blueprint(diamod, url_prefix=f'{modulo0}/dia')

from app.rutas.referenciales.dia.dia_api import diaapi

modulo0 = '/referenciales'
app.register_blueprint(espmod, url_prefix=f'{modulo0}/especialidad')

from app.rutas.referenciales.especialidad.especialidad_api import espapi

modulo0 = '/referenciales'
app.register_blueprint(estdmod, url_prefix=f'{modulo0}/estado_cita')

from app.rutas.referenciales.estado_cita.estado_cita_api import estadoapi

modulo0 = '/referenciales'
app.register_blueprint(agendamedmod, url_prefix=f'{modulo0}/agenda_medica')

from app.rutas.referenciales.agenda_medica.agenda_medica_api import agenda_medica_api

modulo0 = '/referenciales'
app.register_blueprint(salmod, url_prefix=f'{modulo0}/sala_atencion')

from app.rutas.referenciales.sala_atencion.sala_atencion_api import salapi

modulo0 = '/referenciales'
app.register_blueprint(usumod, url_prefix=f'{modulo0}/usuaruio')

from app.rutas.referenciales.usuario.usuario_api import usuarioapi

modulo0 = '/referenciales'
app.register_blueprint(disponibilidad_horariamod, url_prefix=f'{modulo0}/disponibilidad_horaria')

from app.rutas.referenciales.disponibilidad_horaria.disponinilidad_horaria_api import disponibilidad_horaria_api

modulo0 = '/referenciales'
app.register_blueprint(citamod, url_prefix=f'{modulo0}/cita')

from app.rutas.referenciales.cita.cita_api import cita_api


# APIS v1
version1 = '/api/v1'
app.register_blueprint(ciuapi, url_prefix=version1)

app.register_blueprint(aviso_api, url_prefix=version1)

app.register_blueprint(estado_laboralapi, url_prefix=version1)

app.register_blueprint(personaapi, url_prefix=version1)

app.register_blueprint(medicoapi,url_prefix=version1)

app.register_blueprint(pacienteapi, url_prefix=version1)

app.register_blueprint(ocuapi, url_prefix=version1)

app.register_blueprint(turapi, url_prefix=version1)

app.register_blueprint(estapi, url_prefix=version1)

app.register_blueprint(enfapi, url_prefix=version1)

app.register_blueprint(genapi, url_prefix=version1)

app.register_blueprint(diaapi, url_prefix=version1)

app.register_blueprint(espapi, url_prefix=version1)

app.register_blueprint(estadoapi, url_prefix=version1)

app.register_blueprint(agenda_medica_api, url_prefix=version1)

app.register_blueprint(salapi, url_prefix=version1)

app.register_blueprint(usuarioapi, url_prefix=version1)

app.register_blueprint(disponibilidad_horaria_api, url_prefix=version1)

app.register_blueprint(cita_api, url_prefix=version1)