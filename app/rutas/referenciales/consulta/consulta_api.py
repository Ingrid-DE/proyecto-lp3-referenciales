from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.consulta.ConsultaDao import ConsultaDao

consulta_api = Blueprint('consulta_api', __name__)

# Trae todas las consultas
@consulta_api.route('/consultas', methods=['GET'])
def getConsultas():
    consultadao = ConsultaDao()

    try:
        consultas = consultadao.getConsultas()

        return jsonify({
            'success': True,
            'data': consultas,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las consultas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Trae una consulta por ID
@consulta_api.route('/consultas/<int:consulta_id>', methods=['GET'])
def getConsulta(consulta_id):
    consultadao = ConsultaDao()

    try:
        consulta = consultadao.getConsultaById(consulta_id)

        if consulta:
            return jsonify({
                'success': True,
                'data': consulta,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la consulta con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener consulta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Obtener citas disponibles para crear consulta
@consulta_api.route('/consultas/citas-disponibles', methods=['GET'])
def getCitasDisponibles():
    consultadao = ConsultaDao()
    
    try:
        data = consultadao.getCitasDisponibles()
        citas = []
        for row in data:
            citas.append({
                'id_cita': row[0],
                'paciente': row[1],
                'cedula': row[2],
                'medico': row[3],
                'especialidad': row[4],
                'fecha': row[5].strftime('%d/%m/%Y'),
                'hora_inicio': row[6].strftime('%H:%M'),
                'hora_fin': row[7].strftime('%H:%M'),
                'estado_cita': row[8],
                'sala_atencion': row[9]
            })
        return jsonify({
            'success': True,
            'data': citas,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener citas disponibles: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Obtener órdenes de estudio disponibles
@consulta_api.route('/consultas/ordenes-estudio-disponibles', methods=['GET'])
def getOrdenesEstudioDisponibles():
    consultadao = ConsultaDao()
    
    try:
        data = consultadao.getOrdenesEstudioDisponibles()
        ordenes = []
        for row in data:
            ordenes.append({
                'id_orden_estudio': row[0],
                'tipo_estudio': row[1],
                'fecha_emision': row[2].strftime('%d/%m/%Y'),
                'observacion': row[3] if row[3] else '',
                'estado': row[4]
            })
        return jsonify({
            'success': True,
            'data': ordenes,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener órdenes de estudio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Obtener órdenes de análisis disponibles
@consulta_api.route('/consultas/ordenes-analisis-disponibles', methods=['GET'])
def getOrdenesAnalisisDisponibles():
    consultadao = ConsultaDao()
    
    try:
        data = consultadao.getOrdenesAnalisisDisponibles()
        ordenes = []
        for row in data:
            ordenes.append({
                'id_orden_analisis': row[0],
                'tipo_analisis': row[1],
                'fecha_emision': row[2].strftime('%d/%m/%Y'),
                'observacion': row[3] if row[3] else '',
                'estado': row[4]
            })
        return jsonify({
            'success': True,
            'data': ordenes,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener órdenes de análisis: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva consulta
@consulta_api.route('/consultas', methods=['POST'])
def addConsulta():
    data = request.get_json()
    consultadao = ConsultaDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['id_cita', 'motivo_consulta']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        id_cita = data['id_cita']
        id_orden_estudio = data.get('id_orden_estudio', None)
        id_orden_analisis = data.get('id_orden_analisis', None)
        motivo_consulta = data['motivo_consulta']
        diagnostico = data.get('diagnostico', '')
        tratamiento = data.get('tratamiento', '')
        observaciones = data.get('observaciones', '')

        consulta_id = consultadao.guardarConsulta(id_cita, id_orden_estudio, id_orden_analisis, motivo_consulta, diagnostico, tratamiento, observaciones)
        
        if consulta_id:
            return jsonify({
                'success': True,
                'data': {
                    'id_consulta': consulta_id,
                    'id_cita': id_cita,
                    'id_orden_estudio': id_orden_estudio,
                    'id_orden_analisis': id_orden_analisis,
                    'motivo_consulta': motivo_consulta,
                    'diagnostico': diagnostico,
                    'tratamiento': tratamiento,
                    'observaciones': observaciones
                },
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar la consulta. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar consulta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualiza una consulta
@consulta_api.route('/consultas/<int:consulta_id>', methods=['PUT'])
def updateConsulta(consulta_id):
    data = request.get_json()
    consultadao = ConsultaDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['id_cita', 'motivo_consulta']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        id_cita = data['id_cita']
        id_orden_estudio = data.get('id_orden_estudio', None)
        id_orden_analisis = data.get('id_orden_analisis', None)
        motivo_consulta = data['motivo_consulta']
        diagnostico = data.get('diagnostico', '')
        tratamiento = data.get('tratamiento', '')
        observaciones = data.get('observaciones', '')

        if consultadao.updateConsulta(consulta_id, id_cita, id_orden_estudio, id_orden_analisis, motivo_consulta, diagnostico, tratamiento, observaciones):
            return jsonify({
                'success': True,
                'data': {
                    'id_consulta': consulta_id,
                    'id_cita': id_cita,
                    'id_orden_estudio': id_orden_estudio,
                    'id_orden_analisis': id_orden_analisis,
                    'motivo_consulta': motivo_consulta,
                    'diagnostico': diagnostico,
                    'tratamiento': tratamiento,
                    'observaciones': observaciones
                },
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la consulta con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar consulta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Elimina una consulta
@consulta_api.route('/consultas/<int:consulta_id>', methods=['DELETE'])
def deleteConsulta(consulta_id):
    consultadao = ConsultaDao()

    try:
        if consultadao.deleteConsulta(consulta_id):
            return jsonify({
                'success': True,
                'mensaje': f'Consulta con ID {consulta_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la consulta con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar consulta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500