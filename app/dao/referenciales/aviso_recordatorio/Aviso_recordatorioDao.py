from flask import current_app as app
from app.conexion.Conexion import Conexion

class AvisoRecordatorioDao:

    def getAll(self):
        """Obtiene todos los avisos recordatorios"""
        sql = """
        SELECT 
            ar.id_aviso,
            ar.id_cita,
            p.nombre AS paciente_nombre,
            p.apellido AS paciente_apellido,
            perM.nombre AS medico_nombre,
            perM.apellido AS medico_apellido,
            d.fecha,
            d.hora_inicio,
            ar.fecha_programada,
            ar.fecha_envio,
            ar.metodo_envio,
            ar.mensaje,
            ar.estado,
            ar.destinatario,
            ar.intentos_envio,
            e.descripcion AS especialidad
        FROM avisos_recordatorios ar
        INNER JOIN citas c ON ar.id_cita = c.id_cita
        INNER JOIN pacientes pa ON c.id_paciente = pa.id_paciente
        INNER JOIN personas p ON pa.id_persona = p.id_persona
        INNER JOIN disponibilidad_horaria d ON c.id_disponibilidad_horaria = d.id_disponibilidad_horaria
        INNER JOIN agenda_medicas am ON d.id_agenda_medica = am.id_agenda_medica
        INNER JOIN medicos m ON am.id_medico = m.id_medico
        INNER JOIN personas perM ON m.id_persona = perM.id_persona
        INNER JOIN especialidades e ON am.id_especialidad = e.id_especialidad
        ORDER BY ar.fecha_programada DESC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            data = cur.fetchall()
            return data
        except Exception as e:
            app.logger.error(f"Error al obtener avisos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getById(self, id_aviso):
        """Obtiene un aviso por su ID"""
        sql = """
        SELECT 
            ar.id_aviso,
            ar.id_cita,
            p.nombre AS paciente_nombre,
            p.apellido AS paciente_apellido,
            perM.nombre AS medico_nombre,
            perM.apellido AS medico_apellido,
            d.fecha,
            d.hora_inicio,
            ar.fecha_programada,
            ar.fecha_envio,
            ar.metodo_envio,
            ar.mensaje,
            ar.estado,
            ar.destinatario,
            ar.intentos_envio,
            ar.observacion,
            e.descripcion AS especialidad
        FROM avisos_recordatorios ar
        INNER JOIN citas c ON ar.id_cita = c.id_cita
        INNER JOIN pacientes pa ON c.id_paciente = pa.id_paciente
        INNER JOIN personas p ON pa.id_persona = p.id_persona
        INNER JOIN disponibilidad_horaria d ON c.id_disponibilidad_horaria = d.id_disponibilidad_horaria
        INNER JOIN agenda_medicas am ON d.id_agenda_medica = am.id_agenda_medica
        INNER JOIN medicos m ON am.id_medico = m.id_medico
        INNER JOIN personas perM ON m.id_persona = perM.id_persona
        INNER JOIN especialidades e ON am.id_especialidad = e.id_especialidad
        WHERE ar.id_aviso = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_aviso,))
            return cur.fetchone()
        except Exception as e:
            app.logger.error(f"Error al obtener aviso: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def getCitasDisponibles(self):
        """Obtiene las citas que aún no tienen aviso recordatorio"""
        sql = """
        SELECT 
            c.id_cita,
            p.nombre || ' ' || p.apellido AS paciente,
            perM.nombre || ' ' || perM.apellido AS medico,
            e.descripcion AS especialidad,
            d.fecha,
            d.hora_inicio,
            d.hora_fin,
            ec.descripcion AS estado_cita,
            p.telefono_emergencia
        FROM citas c
        INNER JOIN pacientes pa ON c.id_paciente = pa.id_paciente
        INNER JOIN personas p ON pa.id_persona = p.id_persona
        INNER JOIN disponibilidad_horaria d ON c.id_disponibilidad_horaria = d.id_disponibilidad_horaria
        INNER JOIN agenda_medicas am ON d.id_agenda_medica = am.id_agenda_medica
        INNER JOIN medicos m ON am.id_medico = m.id_medico
        INNER JOIN personas perM ON m.id_persona = perM.id_persona
        INNER JOIN especialidades e ON am.id_especialidad = e.id_especialidad
        INNER JOIN estado_citas ec ON c.id_estado_cita = ec.id_estado_cita
        WHERE c.id_cita NOT IN (SELECT id_cita FROM avisos_recordatorios)
        AND d.fecha > CURRENT_DATE
        AND ec.descripcion IN ('Pendiente', 'Confirmada')
        ORDER BY d.fecha, d.hora_inicio
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            return cur.fetchall()
        except Exception as e:
            app.logger.error(f"Error al obtener citas disponibles: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def guardarAviso(self, id_cita, fecha_programada, metodo_envio, mensaje, destinatario):
        """Guarda un nuevo aviso recordatorio"""
        sql = """
        INSERT INTO avisos_recordatorios 
        (id_cita, fecha_programada, metodo_envio, mensaje, estado, destinatario, intentos_envio)
        VALUES (%s, %s, %s, %s, 'pendiente', %s, 0)
        RETURNING id_aviso
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_cita, fecha_programada, metodo_envio, mensaje, destinatario))
            id_aviso = cur.fetchone()[0]
            con.commit()
            return id_aviso
        except Exception as e:
            app.logger.error(f"Error al guardar aviso: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()

    def actualizarAviso(self, id_aviso, fecha_programada, metodo_envio, mensaje, destinatario):
        """Actualiza un aviso existente"""
        sql = """
        UPDATE avisos_recordatorios
        SET fecha_programada = %s, metodo_envio = %s, mensaje = %s, destinatario = %s
        WHERE id_aviso = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (fecha_programada, metodo_envio, mensaje, destinatario, id_aviso))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar aviso: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def eliminarAviso(self, id_aviso):
        """Elimina un aviso recordatorio"""
        sql = "DELETE FROM avisos_recordatorios WHERE id_aviso = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_aviso,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar aviso: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def getAvisosPendientes(self):
        """Obtiene avisos pendientes de envío"""
        sql = """
        SELECT 
            ar.id_aviso,
            p.nombre || ' ' || p.apellido AS paciente,
            p.telefono_emergencia,
            perM.nombre || ' ' || perM.apellido AS medico,
            d.fecha,
            d.hora_inicio,
            ar.metodo_envio,
            ar.mensaje,
            ar.destinatario,
            e.descripcion AS especialidad
        FROM avisos_recordatorios ar
        INNER JOIN citas c ON ar.id_cita = c.id_cita
        INNER JOIN pacientes pa ON c.id_paciente = pa.id_paciente
        INNER JOIN personas p ON pa.id_persona = p.id_persona
        INNER JOIN disponibilidad_horaria d ON c.id_disponibilidad_horaria = d.id_disponibilidad_horaria
        INNER JOIN agenda_medicas am ON d.id_agenda_medica = am.id_agenda_medica
        INNER JOIN medicos m ON am.id_medico = m.id_medico
        INNER JOIN personas perM ON m.id_persona = perM.id_persona
        INNER JOIN especialidades e ON am.id_especialidad = e.id_especialidad
        WHERE ar.estado = 'pendiente' 
        AND ar.fecha_programada <= NOW()
        AND ar.intentos_envio < 3
        ORDER BY ar.fecha_programada
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            return cur.fetchall()
        except Exception as e:
            app.logger.error(f"Error al obtener avisos pendientes: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def enviarAvisoWhatsApp(self, id_aviso):
        """Simula el envío del aviso por WhatsApp y actualiza estado/envío"""
        updateSQL = """
        UPDATE avisos_recordatorios
        SET estado = 'enviado', 
            fecha_envio = NOW(),
            intentos_envio = intentos_envio + 1
        WHERE id_aviso = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            aviso = self.getById(id_aviso)
            if not aviso:
                return False

            # Construir mensaje
            mensaje = (
                f"📅 *Recordatorio de Cita Médica*\n\n"
                f"Hola {aviso[2]} {aviso[3]}, te recordamos tu cita:\n\n"
                f"👨‍⚕️ Doctor: {aviso[4]} {aviso[5]}\n"
                f"🏥 Especialidad: {aviso[16]}\n"
                f"📆 Fecha: {aviso[6].strftime('%d/%m/%Y')}\n"
                f"🕐 Hora: {aviso[7].strftime('%H:%M')} hs\n\n"
                f"Por favor, confirmá tu asistencia o comunicate si necesitás reprogramar.\n\n"
                f"¡Te esperamos! 😊"
            )

            telefono = aviso[13] if aviso[13] else "Sin teléfono"
            app.logger.info(f"Simulando envío WhatsApp a {telefono}:\n{mensaje}")
            print(f"\n{'='*50}\nENVÍO SIMULADO - WhatsApp\n{'='*50}")
            print(f"Destinatario: {telefono}")
            print(f"Mensaje:\n{mensaje}")
            print(f"{'='*50}\n")

            cur.execute(updateSQL, (id_aviso,))
            con.commit()
            return True
        except Exception as e:
            app.logger.error(f"Error al enviar aviso WhatsApp: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def marcarComoFallido(self, id_aviso, observacion):
        """Marca un aviso como fallido"""
        sql = """
        UPDATE avisos_recordatorios
        SET estado = 'fallido',
            intentos_envio = intentos_envio + 1,
            observacion = %s
        WHERE id_aviso = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (observacion, id_aviso))
            con.commit()
            return True
        except Exception as e:
            app.logger.error(f"Error al marcar como fallido: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()