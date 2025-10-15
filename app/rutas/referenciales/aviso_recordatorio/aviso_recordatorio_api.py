from flask import Blueprint, jsonify, request, current_app as app
from app.dao.referenciales.aviso_recordatorio.Aviso_recordatorioDao import AvisoRecordatorioDao
from datetime import datetime, timedelta

aviso_api = Blueprint('aviso_api', __name__)

@aviso_api.route('/avisos', methods=['GET'])
def getAvisos():
    """Obtiene todos los avisos recordatorios"""
    dao = AvisoRecordatorioDao()
    data = dao.getAll()
    avisos = []
    for row in data:
        avisos.append({
            'id_aviso': row[0],
            'id_cita': row[1],
            'paciente': f"{row[2]} {row[3]}",
            'medico': f"{row[4]} {row[5]}",
            'fecha': row[6].strftime('%d/%m/%Y'),
            'hora': row[7].strftime('%H:%M'),
            'fecha_programada': row[8].strftime('%d/%m/%Y %H:%M'),
            'fecha_envio': row[9].strftime('%d/%m/%Y %H:%M') if row[9] else '',
            'metodo_envio': row[10],
            'mensaje': row[11],
            'estado': row[12],
            'destinatario': row[13] if row[13] else '',
            'intentos_envio': row[14],
            'especialidad': row[15]
        })
    return jsonify({
        'success': True,
        'data': avisos,
        'error': None
    }), 200

@aviso_api.route('/avisos/<int:id_aviso>', methods=['GET'])
def getAviso(id_aviso):
    """Obtiene un aviso por su ID"""
    dao = AvisoRecordatorioDao()
    row = dao.getById(id_aviso)
    
    if not row:
        return jsonify({
            'success': False,
            'error': 'Aviso no encontrado'
        }), 404
    
    aviso = {
        'id_aviso': row[0],
        'id_cita': row[1],
        'paciente': f"{row[2]} {row[3]}",
        'medico': f"{row[4]} {row[5]}",
        'fecha': row[6].strftime('%Y-%m-%d'),
        'hora': row[7].strftime('%H:%M'),
        'fecha_programada': row[8].strftime('%Y-%m-%dT%H:%M'),
        'fecha_envio': row[9].strftime('%d/%m/%Y %H:%M') if row[9] else '',
        'metodo_envio': row[10],
        'mensaje': row[11],
        'estado': row[12],
        'destinatario': row[13] if row[13] else '',
        'intentos_envio': row[14],
        'observacion': row[15] if row[15] else '',
        'especialidad': row[16]
    }
    
    return jsonify({
        'success': True,
        'data': aviso,
        'error': None
    }), 200

@aviso_api.route('/avisos/citas-disponibles', methods=['GET'])
def getCitasDisponibles():
    """Obtiene citas que aún no tienen aviso"""
    dao = AvisoRecordatorioDao()
    data = dao.getCitasDisponibles()
    citas = []
    for row in data:
        citas.append({
            'id_cita': row[0],
            'paciente': row[1],
            'medico': row[2],
            'especialidad': row[3],
            'fecha': row[4].strftime('%d/%m/%Y'),
            'hora_inicio': row[5].strftime('%H:%M'),
            'hora_fin': row[6].strftime('%H:%M'),
            'estado_cita': row[7],
            'telefono': row[8] if row[8] else ''
        })
    return jsonify({
        'success': True,
        'data': citas,
        'error': None
    }), 200

@aviso_api.route('/avisos', methods=['POST'])
def crearAviso():
    """Crea un nuevo aviso recordatorio"""
    data = request.get_json()
    dao = AvisoRecordatorioDao()
    
    # Validar campos requeridos
    campos_requeridos = ['id_cita', 'fecha_programada', 'metodo_envio', 'destinatario']
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio'
            }), 400
    
    try:
        id_cita = data['id_cita']
        fecha_programada = data['fecha_programada']
        metodo_envio = data['metodo_envio']
        mensaje = data.get('mensaje', '')
        destinatario = data['destinatario']
        
        # Si no hay mensaje, crear uno por defecto
        if not mensaje:
            mensaje = "Recordatorio de cita médica. Por favor, confirme su asistencia."
        
        id_aviso = dao.guardarAviso(id_cita, fecha_programada, metodo_envio, mensaje, destinatario)
        
        if id_aviso:
            return jsonify({
                'success': True,
                'data': {'id_aviso': id_aviso},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo crear el aviso'
            }), 500
            
    except Exception as e:
        app.logger.error(f"Error al crear aviso: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno al crear el aviso'
        }), 500

@aviso_api.route('/avisos/<int:id_aviso>', methods=['PUT'])
def actualizarAviso(id_aviso):
    """Actualiza un aviso existente"""
    data = request.get_json()
    dao = AvisoRecordatorioDao()
    
    # Validar campos requeridos
    campos_requeridos = ['fecha_programada', 'metodo_envio', 'destinatario']
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio'
            }), 400
    
    try:
        fecha_programada = data['fecha_programada']
        metodo_envio = data['metodo_envio']
        mensaje = data.get('mensaje', '')
        destinatario = data['destinatario']
        
        exito = dao.actualizarAviso(id_aviso, fecha_programada, metodo_envio, mensaje, destinatario)
        
        if exito:
            return jsonify({
                'success': True,
                'message': 'Aviso actualizado correctamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el aviso'
            }), 404
            
    except Exception as e:
        app.logger.error(f"Error al actualizar aviso: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno al actualizar el aviso'
        }), 500

@aviso_api.route('/avisos/<int:id_aviso>', methods=['DELETE'])
def eliminarAviso(id_aviso):
    """Elimina un aviso recordatorio"""
    dao = AvisoRecordatorioDao()
    try:
        exito = dao.eliminarAviso(id_aviso)
        if exito:
            return jsonify({
                'success': True,
                'message': 'Aviso eliminado correctamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el aviso'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar aviso: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno al eliminar el aviso'
        }), 500

@aviso_api.route('/avisos/enviar/<int:id_aviso>', methods=['POST'])
def enviarAviso(id_aviso):
    """Envía un aviso por WhatsApp (simulado)"""
    dao = AvisoRecordatorioDao()
    try:
        exito = dao.enviarAvisoWhatsApp(id_aviso)
        if exito:
            return jsonify({
                'success': True,
                'message': 'Aviso enviado correctamente (simulado)',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo enviar el aviso'
            }), 400
    except Exception as e:
        app.logger.error(f"Error al enviar aviso: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno al enviar el aviso'
        }), 500

@aviso_api.route('/avisos/pendientes', methods=['GET'])
def getAvisosPendientes():
    """Obtiene avisos pendientes de envío"""
    dao = AvisoRecordatorioDao()
    data = dao.getAvisosPendientes()
    avisos = []
    for row in data:
        avisos.append({
            'id_aviso': row[0],
            'paciente': row[1],
            'telefono': row[2],
            'medico': row[3],
            'fecha_cita': row[4].strftime('%d/%m/%Y'),
            'hora': row[5].strftime('%H:%M'),
            'metodo_envio': row[6],
            'mensaje': row[7],
            'destinatario': row[8],
            'especialidad': row[9]
        })
    return jsonify({
        'success': True,
        'data': avisos,
        'error': None
    }), 200

@aviso_api.route('/avisos/marcar-fallido/<int:id_aviso>', methods=['PUT'])
def marcarFallido(id_aviso):
    """Marca un aviso como fallido"""
    data = request.get_json()
    observacion = data.get('observacion', 'Error al enviar aviso')
    
    dao = AvisoRecordatorioDao()
    try:
        exito = dao.marcarComoFallido(id_aviso, observacion)
        if exito:
            return jsonify({
                'success': True,
                'message': 'Aviso marcado como fallido',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el aviso'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al marcar como fallido: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno'
        }), 500