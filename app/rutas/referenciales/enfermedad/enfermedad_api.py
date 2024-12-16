from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.enfermedad.EnfermedadDao import EnfermedadDao

enfapi = Blueprint('enfapi', __name__)

# Trae todas las ciudades
@enfapi.route('/enfermedades', methods=['GET'])
def getEnfermedades():
    enfdao = EnfermedadDao()

    try:
        enfermedades = enfdao.getEnfermedad()

        return jsonify({
            'success': True,
            'data': enfermedades,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las enfermedades: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@enfapi.route('/enfermedades/<int:enfermedad_id>', methods=['GET'])
def getEnfermedad(enfermedad_id):
    enfdao = EnfermedadDao()

    try:
        enfermedad =enfdao.getEnfermedadById(enfermedad_id)

        if enfermedad:
            return jsonify({
                'success': True,
                'data': enfermedad,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la enfermedad con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener enfermedad: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva ciudad
@enfapi.route('/enfermedades', methods=['POST'])
def addEnfermedad():
    data = request.get_json()
    enfdao = EnfermedadDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        descripcion = data['descripcion'].upper()
        enfermedad_id = enfdao.guardarEnfermedad(descripcion)
        if enfermedad_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': enfermedad_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar la enfermedad del paciente. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar la enfermedad del paciente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@enfapi.route('/enfermedades/<int:enfermedad_id>', methods=['PUT'])
def updateEnfermedad(enfermedad_id):
    data = request.get_json()
    enfdao = EnfermedadDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400
    descripcion = data['descripcion']
    try:
        if enfdao.updateEnfermedad(enfermedad_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': enfermedad_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la enfermedad con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar  la enfermedad del paciente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@enfapi.route('/enfermedades/<int:enfermedad_id>', methods=['DELETE'])
def deleteEnfermedad(enfermedad_id):
    enfdao = EnfermedadDao()

    try:
        # Usar el retorno de eliminarCiudad para determinar el éxito
        if enfdao.deleteEnfermedad(enfermedad_id):
            return jsonify({
                'success': True,
                'mensaje': f'enfermedad con ID {enfermedad_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la enfermedad del paciente con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar la enfermedad del paciente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500