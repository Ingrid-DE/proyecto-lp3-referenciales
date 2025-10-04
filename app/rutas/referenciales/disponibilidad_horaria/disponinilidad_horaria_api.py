from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.disponibilidad_horaria.Disponibilidad_horariaDao import Disponibilidad_horariaDao
from datetime import date, time

disponibilidad_horaria_api = Blueprint('disponibilidad_horaria_api', __name__)

# Función auxiliar para convertir datos a formato JSON serializable
def convertir_a_dict(row):
    return {
        'id_disponibilidad_horaria': row[0],
        'fecha': str(row[1]) if row[1] else None,
        'hora_inicio': str(row[2]) if row[2] else None,
        'hora_fin': str(row[3]) if row[3] else None,
        'estado': row[4],
        'id_agenda_medica': row[5],
        'medico': row[6],
        'especialidad': row[7],
        'dia': row[8],
        'turno': row[9],
        'sala': row[10],
        'estado_laboral': row[11]
    }

# Función auxiliar para convertir disponibilidad simple
def convertir_disponibilidad_simple(row):
    return {
        'id_disponibilidad_horaria': row[0],
        'id_agenda_medica': row[1],
        'fecha': str(row[2]) if row[2] else None,
        'hora_inicio': str(row[3]) if row[3] else None,
        'hora_fin': str(row[4]) if row[4] else None,
        'estado': row[5]
    }

# Trae todas las disponibilidades horarias
@disponibilidad_horaria_api.route('/disponibilidades', methods=['GET'])
def getDisponibilidades():
    disponibilidaddao = Disponibilidad_horariaDao()
    try:
        disponibilidades = disponibilidaddao.getDisponibilidades()
        disponibilidades_list = [convertir_a_dict(row) for row in disponibilidades or []]

        return jsonify({
            'success': True,
            'data': disponibilidades_list,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error en endpoint GET /disponibilidades: {str(e)}")
        import traceback
        app.logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'data': None,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Trae una disponibilidad por ID
@disponibilidad_horaria_api.route('/disponibilidades/<int:disponibilidad_id>', methods=['GET'])
def getDisponibilidad(disponibilidad_id):
    disponibilidaddao = Disponibilidad_horariaDao()
    try:
        disponibilidad = disponibilidaddao.getDisponibilidadById(disponibilidad_id)
        if disponibilidad:
            disponibilidad_dict = convertir_disponibilidad_simple(disponibilidad)
            return jsonify({
                'success': True,
                'data': disponibilidad_dict,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'data': None,
                'error': 'No se encontró la disponibilidad con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error en endpoint GET /disponibilidades/{disponibilidad_id}: {str(e)}")
        import traceback
        app.logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'data': None,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Trae disponibilidades por agenda médica
@disponibilidad_horaria_api.route('/disponibilidades/agenda/<int:agenda_id>', methods=['GET'])
def getDisponibilidadesPorAgenda(agenda_id):
    disponibilidaddao = Disponibilidad_horariaDao()
    fecha = request.args.get('fecha', None)
    try:
        disponibilidades = disponibilidaddao.getDisponibilidadesPorAgenda(agenda_id, fecha)
        disponibilidades_list = [convertir_disponibilidad_simple(row) for row in disponibilidades or []]

        return jsonify({
            'success': True,
            'data': disponibilidades_list,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error en endpoint GET /disponibilidades/agenda/{agenda_id}: {str(e)}")
        import traceback
        app.logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'data': None,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva disponibilidad horaria
@disponibilidad_horaria_api.route('/disponibilidades', methods=['POST'])
def addDisponibilidad():
    disponibilidaddao = Disponibilidad_horariaDao()
    data = request.get_json()

    try:
        nueva_disponibilidad = disponibilidaddao.addDisponibilidad(data)

        # Convertir fechas y horas a string si existen
        if nueva_disponibilidad:
            if 'fecha' in nueva_disponibilidad and isinstance(nueva_disponibilidad['fecha'], date):
                nueva_disponibilidad['fecha'] = str(nueva_disponibilidad['fecha'])
            if 'hora_inicio' in nueva_disponibilidad and isinstance(nueva_disponibilidad['hora_inicio'], time):
                nueva_disponibilidad['hora_inicio'] = str(nueva_disponibilidad['hora_inicio'])
            if 'hora_fin' in nueva_disponibilidad and isinstance(nueva_disponibilidad['hora_fin'], time):
                nueva_disponibilidad['hora_fin'] = str(nueva_disponibilidad['hora_fin'])

        return jsonify({
            'success': True,
            'data': nueva_disponibilidad,
            'error': None
        }), 201
    except Exception as e:
        app.logger.error(f"Error en endpoint POST /disponibilidades: {str(e)}")
        import traceback
        app.logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'data': None,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# 🔁 ACTUALIZAR una disponibilidad horaria
@disponibilidad_horaria_api.route('/disponibilidades/<int:disponibilidad_id>', methods=['PUT'])
def updateDisponibilidad(disponibilidad_id):
    disponibilidaddao = Disponibilidad_horariaDao()
    data = request.get_json()

    try:
        disponibilidad_actualizada = disponibilidaddao.updateDisponibilidad(disponibilidad_id, data)
        if disponibilidad_actualizada:
            return jsonify({
                'success': True,
                'data': disponibilidad_actualizada,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'data': None,
                'error': 'No se encontró la disponibilidad para actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error en PUT /disponibilidades/{disponibilidad_id}: {str(e)}")
        import traceback
        app.logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'data': None,
            'error': 'Error interno al actualizar la disponibilidad.'
        }), 500

# ❌ ELIMINAR una disponibilidad horaria
@disponibilidad_horaria_api.route('/disponibilidades/<int:disponibilidad_id>', methods=['DELETE'])
def deleteDisponibilidad(disponibilidad_id):
    disponibilidaddao = Disponibilidad_horariaDao()

    try:
        eliminado = disponibilidaddao.deleteDisponibilidad(disponibilidad_id)
        if eliminado:
            return jsonify({
                'success': True,
                'data': f'Disponibilidad {disponibilidad_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'data': None,
                'error': 'No se encontró la disponibilidad para eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error en DELETE /disponibilidades/{disponibilidad_id}: {str(e)}")
        import traceback
        app.logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'data': None,
            'error': 'Error interno al eliminar la disponibilidad.'
        }), 500
