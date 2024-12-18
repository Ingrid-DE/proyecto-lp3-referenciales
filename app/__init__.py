from datetime import timedelta
from flask import Flask
app = Flask(__name__)

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
from app.rutas.referenciales.hora.hora_routes import hormod
from app.rutas.referenciales.especialidad.especialidad_routes import espmod
from app.rutas.referenciales.estado_cita.estado_cita_routes import estdmod
from app.rutas.referenciales.estado_laboral.estado_laboral_routes import estado_laboralmod
from app.rutas.referenciales.ficha.ficha_routes import fichamod
from app.rutas.referenciales.agenda_medica.agenda_medica_routes import agendamedmod
from app.rutas.referenciales.sala_atencion.sala_atencion_routes import salmod

# registrar referenciales
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
app.register_blueprint(hormod, url_prefix=f'{modulo0}/hora')

from app.rutas.referenciales.hora.hora_api import horapi

modulo0 = '/referenciales'
app.register_blueprint(espmod, url_prefix=f'{modulo0}/especialidad')

from app.rutas.referenciales.especialidad.especialidad_api import espapi

modulo0 = '/referenciales'
app.register_blueprint(estdmod, url_prefix=f'{modulo0}/estado_cita')

from app.rutas.referenciales.estado_cita.estado_cita_api import estadoapi

modulo0 = '/referenciales'
app.register_blueprint(fichamod, url_prefix=f'{modulo0}/ficha')

from app.rutas.referenciales.ficha.ficha_api import fichaapi

modulo0 = '/referenciales'
app.register_blueprint(agendamedmod, url_prefix=f'{modulo0}/agenda_medica')

from app.rutas.referenciales.agenda_medica.agenda_medica_api import agenda_medica_api

modulo0 = '/referenciales'
app.register_blueprint(salmod, url_prefix=f'{modulo0}/sala_atencion')

from app.rutas.referenciales.sala_atencion.sala_atencion_api import salapi

# APIS v1
version1 = '/api/v1'
app.register_blueprint(ciuapi, url_prefix=version1)

version1 = '/api/v1'
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

app.register_blueprint(horapi, url_prefix=version1)

app.register_blueprint(espapi, url_prefix=version1)

app.register_blueprint(estadoapi, url_prefix=version1)

app.register_blueprint(fichaapi, url_prefix=version1)

app.register_blueprint(agenda_medica_api, url_prefix=version1)

app.register_blueprint(salapi, url_prefix=version1)