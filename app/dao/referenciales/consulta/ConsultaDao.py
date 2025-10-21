# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class ConsultaDao:

    def getConsultas(self):
        """Obtiene todas las consultas con información completa"""
        consultaSQL = """
        SELECT 
            co.id_consulta,
            co.id_cita,
            p.nombre || ' ' || p.apellido AS paciente,
            perM.nombre || ' ' || perM.apellido AS medico,
            e.descripcion AS especialidad,
            dh.fecha,
            dh.hora_inicio,
            co.motivo_consulta,
            co.diagnostico,
            co.tratamiento,
            co.observaciones,
            co.fecha_consulta,
            COALESCE(toe.descripcion, 'Sin orden') AS tipo_estudio,
            COALESCE(toa.descripcion, 'Sin orden') AS tipo_analisis,
            ec.descripcion AS estado_cita
        FROM consultas co
        INNER JOIN citas c ON co.id_cita = c.id_cita
        INNER JOIN pacientes pa ON c.id_paciente = pa.id_paciente
        INNER JOIN personas p ON pa.id_persona = p.id_persona
        INNER JOIN disponibilidad_horaria dh ON c.id_disponibilidad_horaria = dh.id_disponibilidad_horaria
        INNER JOIN agenda_medicas am ON dh.id_agenda_medica = am.id_agenda_medica
        INNER JOIN medicos m ON am.id_medico = m.id_medico
        INNER JOIN personas perM ON m.id_persona = perM.id_persona
        INNER JOIN especialidades e ON am.id_especialidad = e.id_especialidad
        INNER JOIN estado_citas ec ON c.id_estado_cita = ec.id_estado_cita
        LEFT JOIN orden_estudio oe ON co.id_orden_estudio = oe.id_orden_estudio
        LEFT JOIN tipo_orden_estudio toe ON oe.id_tipo_orden_estudio = toe.id_tipo_orden_estudio
        LEFT JOIN orden_analisis oa ON co.id_orden_analisis = oa.id_orden_analisis
        LEFT JOIN tipo_orden_analisis toa ON oa.id_tipo_orden_analisis = toa.id_tipo_orden_analisis
        ORDER BY co.fecha_consulta DESC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(consultaSQL)
            consultas = cur.fetchall()
            return [{
                'id_consulta': consulta[0],
                'id_cita': consulta[1],
                'paciente': consulta[2],
                'medico': consulta[3],
                'especialidad': consulta[4],
                'fecha': consulta[5].strftime('%d/%m/%Y') if consulta[5] else '',
                'hora': consulta[6].strftime('%H:%M') if consulta[6] else '',
                'motivo_consulta': consulta[7],
                'diagnostico': consulta[8],
                'tratamiento': consulta[9],
                'observaciones': consulta[10],
                'fecha_consulta': consulta[11].strftime('%d/%m/%Y %H:%M') if consulta[11] else '',
                'tipo_estudio': consulta[12],
                'tipo_analisis': consulta[13],
                'estado_cita': consulta[14]
            } for consulta in consultas]
        
        except Exception as e:
            app.logger.error(f"Error al obtener todas las consultas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getConsultaById(self, id_consulta):
        """Obtiene una consulta por su ID"""
        consultaSQL = """
        SELECT 
            co.id_consulta,
            co.id_cita,
            p.nombre || ' ' || p.apellido AS paciente,
            perM.nombre || ' ' || perM.apellido AS medico,
            e.descripcion AS especialidad,
            dh.fecha,
            dh.hora_inicio,
            co.motivo_consulta,
            co.diagnostico,
            co.tratamiento,
            co.observaciones,
            co.fecha_consulta,
            co.id_orden_estudio,
            co.id_orden_analisis,
            COALESCE(toe.descripcion, 'Sin orden') AS tipo_estudio,
            COALESCE(toa.descripcion, 'Sin orden') AS tipo_analisis
        FROM consultas co
        INNER JOIN citas c ON co.id_cita = c.id_cita
        INNER JOIN pacientes pa ON c.id_paciente = pa.id_paciente
        INNER JOIN personas p ON pa.id_persona = p.id_persona
        INNER JOIN disponibilidad_horaria dh ON c.id_disponibilidad_horaria = dh.id_disponibilidad_horaria
        INNER JOIN agenda_medicas am ON dh.id_agenda_medica = am.id_agenda_medica
        INNER JOIN medicos m ON am.id_medico = m.id_medico
        INNER JOIN personas perM ON m.id_persona = perM.id_persona
        INNER JOIN especialidades e ON am.id_especialidad = e.id_especialidad
        LEFT JOIN orden_estudio oe ON co.id_orden_estudio = oe.id_orden_estudio
        LEFT JOIN tipo_orden_estudio toe ON oe.id_tipo_orden_estudio = toe.id_tipo_orden_estudio
        LEFT JOIN orden_analisis oa ON co.id_orden_analisis = oa.id_orden_analisis
        LEFT JOIN tipo_orden_analisis toa ON oa.id_tipo_orden_analisis = toa.id_tipo_orden_analisis
        WHERE co.id_consulta = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(consultaSQL, (id_consulta,))
            consultaEncontrada = cur.fetchone()
            if consultaEncontrada:
                return {
                    "id_consulta": consultaEncontrada[0],
                    "id_cita": consultaEncontrada[1],
                    "paciente": consultaEncontrada[2],
                    "medico": consultaEncontrada[3],
                    "especialidad": consultaEncontrada[4],
                    "fecha": consultaEncontrada[5].strftime('%Y-%m-%d') if consultaEncontrada[5] else '',
                    "hora": consultaEncontrada[6].strftime('%H:%M') if consultaEncontrada[6] else '',
                    "motivo_consulta": consultaEncontrada[7],
                    "diagnostico": consultaEncontrada[8],
                    "tratamiento": consultaEncontrada[9],
                    "observaciones": consultaEncontrada[10],
                    "fecha_consulta": consultaEncontrada[11].strftime('%Y-%m-%dT%H:%M') if consultaEncontrada[11] else '',
                    "id_orden_estudio": consultaEncontrada[12],
                    "id_orden_analisis": consultaEncontrada[13],
                    "tipo_estudio": consultaEncontrada[14],
                    "tipo_analisis": consultaEncontrada[15]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener consulta: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def getCitasDisponibles(self):
        """Obtiene TODAS las citas que aún no tienen consulta registrada"""
        citasSQL = """
        SELECT 
            c.id_cita,
            p.nombre || ' ' || p.apellido AS paciente,
            p.cedula,
            perM.nombre || ' ' || perM.apellido AS medico,
            e.descripcion AS especialidad,
            dh.fecha,
            dh.hora_inicio,
            dh.hora_fin,
            ec.descripcion AS estado_cita,
            sa.nombre AS sala_atencion
        FROM citas c
        INNER JOIN pacientes pa ON c.id_paciente = pa.id_paciente
        INNER JOIN personas p ON pa.id_persona = p.id_persona
        INNER JOIN disponibilidad_horaria dh ON c.id_disponibilidad_horaria = dh.id_disponibilidad_horaria
        INNER JOIN agenda_medicas am ON dh.id_agenda_medica = am.id_agenda_medica
        INNER JOIN medicos m ON am.id_medico = m.id_medico
        INNER JOIN personas perM ON m.id_persona = perM.id_persona
        INNER JOIN especialidades e ON am.id_especialidad = e.id_especialidad
        INNER JOIN estado_citas ec ON c.id_estado_cita = ec.id_estado_cita
        INNER JOIN sala_atenciones sa ON am.id_sala_atencion = sa.id_sala_atencion
        WHERE c.id_cita NOT IN (SELECT id_cita FROM consultas)
        ORDER BY dh.fecha DESC, dh.hora_inicio DESC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(citasSQL)
            return cur.fetchall()
        except Exception as e:
            app.logger.error(f"Error al obtener citas disponibles: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getOrdenesEstudioDisponibles(self):
        """Obtiene TODAS las órdenes de estudio disponibles"""
        ordenesSQL = """
        SELECT 
            oe.id_orden_estudio,
            toe.descripcion,
            oe.fecha_emision,
            oe.observacion,
            oe.estado
        FROM orden_estudio oe
        INNER JOIN tipo_orden_estudio toe ON oe.id_tipo_orden_estudio = toe.id_tipo_orden_estudio
        ORDER BY oe.fecha_emision DESC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(ordenesSQL)
            return cur.fetchall()
        except Exception as e:
            app.logger.error(f"Error al obtener órdenes de estudio: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getOrdenesAnalisisDisponibles(self):
        """Obtiene TODAS las órdenes de análisis disponibles"""
        ordenesSQL = """
        SELECT 
            oa.id_orden_analisis,
            toa.descripcion,
            oa.fecha_emision,
            oa.observacion,
            oa.estado
        FROM orden_analisis oa
        INNER JOIN tipo_orden_analisis toa ON oa.id_tipo_orden_analisis = toa.id_tipo_orden_analisis
        ORDER BY oa.fecha_emision DESC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(ordenesSQL)
            return cur.fetchall()
        except Exception as e:
            app.logger.error(f"Error al obtener órdenes de análisis: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def guardarConsulta(self, id_cita, id_orden_estudio, id_orden_analisis, motivo_consulta, diagnostico, tratamiento, observaciones):
        """Guarda una nueva consulta médica"""
        insertConsultaSQL = """
        INSERT INTO consultas(id_cita, id_orden_estudio, id_orden_analisis, motivo_consulta, diagnostico, tratamiento, observaciones)
        VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id_consulta
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            # Convertir valores vacíos a NULL
            id_orden_estudio = id_orden_estudio if id_orden_estudio else None
            id_orden_analisis = id_orden_analisis if id_orden_analisis else None
            
            cur.execute(insertConsultaSQL, (id_cita, id_orden_estudio, id_orden_analisis, motivo_consulta, diagnostico, tratamiento, observaciones))
            consulta_id = cur.fetchone()[0]
            con.commit()
            return consulta_id
        except Exception as e:
            app.logger.error(f"Error al insertar consulta: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateConsulta(self, id_consulta, id_cita, id_orden_estudio, id_orden_analisis, motivo_consulta, diagnostico, tratamiento, observaciones):
        """Actualiza una consulta existente"""
        updateConsultaSQL = """
        UPDATE consultas
        SET id_cita=%s, id_orden_estudio=%s, id_orden_analisis=%s, motivo_consulta=%s, diagnostico=%s, tratamiento=%s, observaciones=%s
        WHERE id_consulta=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            # Convertir valores vacíos a NULL
            id_orden_estudio = id_orden_estudio if id_orden_estudio else None
            id_orden_analisis = id_orden_analisis if id_orden_analisis else None
            
            cur.execute(updateConsultaSQL, (id_cita, id_orden_estudio, id_orden_analisis, motivo_consulta, diagnostico, tratamiento, observaciones, id_consulta))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar consulta: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteConsulta(self, id_consulta):
        """Elimina una consulta"""
        deleteConsultaSQL = """
        DELETE FROM consultas
        WHERE id_consulta=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(deleteConsultaSQL, (id_consulta,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar consulta: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()