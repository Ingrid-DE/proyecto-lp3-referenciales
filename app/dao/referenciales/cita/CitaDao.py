# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class CitaDao:

    def getCitas(self):
        citaSQL = """
        SELECT 
            c.id_cita,
            p.nombre,
            p.apellido,
            med.nombre AS medico_nombre,
            med.apellido AS medico_apellido,
            e.descripcion AS especialidad,
            dh.fecha,
            dh.hora_inicio,
            dh.hora_fin,
            c.fecha_creacion,
            c.observacion,
            ec.descripcion AS estado_cita
        FROM citas c
        INNER JOIN pacientes pac ON c.id_paciente = pac.id_paciente
        INNER JOIN personas p ON pac.id_persona = p.id_persona
        INNER JOIN disponibilidad_horaria dh ON c.id_disponibilidad_horaria = dh.id_disponibilidad_horaria
        INNER JOIN agenda_medicas am ON dh.id_agenda_medica = am.id_agenda_medica
        INNER JOIN medicos m ON am.id_medico = m.id_medico
        INNER JOIN personas med ON m.id_persona = med.id_persona
        INNER JOIN especialidades e ON am.id_especialidad = e.id_especialidad
        INNER JOIN estado_citas ec ON c.id_estado_cita = ec.id_estado_cita
        ORDER BY c.fecha_creacion DESC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(citaSQL)
            citas = cur.fetchall()
            return [{
                'id_cita': cita[0],
                'paciente_nombre': cita[1],
                'paciente_apellido': cita[2],
                'medico_nombre': cita[3],
                'medico_apellido': cita[4],
                'especialidad': cita[5],
                'fecha': str(cita[6]),
                'hora_inicio': str(cita[7]),
                'hora_fin': str(cita[8]),
                'fecha_creacion': str(cita[9]),
                'observacion': cita[10],
                'estado_cita': cita[11]
            } for cita in citas]
        
        except Exception as e:
            app.logger.error(f"Error al obtener todas las citas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getCitaById(self, id_cita):
        citaSQL = """
        SELECT 
            c.id_cita,
            p.nombre,
            p.apellido,
            med.nombre AS medico_nombre,
            med.apellido AS medico_apellido,
            e.descripcion AS especialidad,
            dh.fecha,
            dh.hora_inicio,
            dh.hora_fin,
            c.fecha_creacion,
            c.observacion,
            ec.descripcion AS estado_cita,
            c.id_disponibilidad_horaria,
            c.id_paciente,
            c.id_estado_cita
        FROM citas c
        INNER JOIN pacientes pac ON c.id_paciente = pac.id_paciente
        INNER JOIN personas p ON pac.id_persona = p.id_persona
        INNER JOIN disponibilidad_horaria dh ON c.id_disponibilidad_horaria = dh.id_disponibilidad_horaria
        INNER JOIN agenda_medicas am ON dh.id_agenda_medica = am.id_agenda_medica
        INNER JOIN medicos m ON am.id_medico = m.id_medico
        INNER JOIN personas med ON m.id_persona = med.id_persona
        INNER JOIN especialidades e ON am.id_especialidad = e.id_especialidad
        INNER JOIN estado_citas ec ON c.id_estado_cita = ec.id_estado_cita
        WHERE c.id_cita = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(citaSQL, (id_cita,))
            citaEncontrada = cur.fetchone()
            if citaEncontrada:
                return {
                    "id_cita": citaEncontrada[0],
                    "paciente_nombre": citaEncontrada[1],
                    "paciente_apellido": citaEncontrada[2],
                    "medico_nombre": citaEncontrada[3],
                    "medico_apellido": citaEncontrada[4],
                    "especialidad": citaEncontrada[5],
                    "fecha": str(citaEncontrada[6]),
                    "hora_inicio": str(citaEncontrada[7]),
                    "hora_fin": str(citaEncontrada[8]),
                    "fecha_creacion": str(citaEncontrada[9]),
                    "observacion": citaEncontrada[10],
                    "estado_cita": citaEncontrada[11],
                    "id_disponibilidad_horaria": citaEncontrada[12],
                    "id_paciente": citaEncontrada[13],
                    "id_estado_cita": citaEncontrada[14]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener cita: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def guardarCita(self, id_disponibilidad_horaria, id_paciente, observacion, id_estado_cita):
        """Guarda una cita y marca la disponibilidad como NO DISPONIBLE"""
        insertCitaSQL = """
        INSERT INTO citas(id_disponibilidad_horaria, id_paciente, observacion, id_estado_cita) 
        VALUES(%s, %s, %s, %s) RETURNING id_cita
        """
        updateDisponibilidadSQL = """
        UPDATE disponibilidad_horaria
        SET estado = FALSE
        WHERE id_disponibilidad_horaria = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            # 1. Verificar que la disponibilidad esté disponible
            cur.execute("SELECT estado FROM disponibilidad_horaria WHERE id_disponibilidad_horaria = %s", 
                       (id_disponibilidad_horaria,))
            resultado = cur.fetchone()
            
            if not resultado:
                app.logger.error("La disponibilidad horaria no existe")
                return False
                
            if not resultado[0]:  # Si estado es FALSE
                app.logger.error("La disponibilidad horaria ya está ocupada")
                return False
            
            # 2. Insertar la cita
            cur.execute(insertCitaSQL, (id_disponibilidad_horaria, id_paciente, observacion, id_estado_cita))
            cita_id = cur.fetchone()[0]
            
            # 3. Marcar la disponibilidad como NO DISPONIBLE
            cur.execute(updateDisponibilidadSQL, (id_disponibilidad_horaria,))
            
            con.commit()
            return cita_id
        except Exception as e:
            app.logger.error(f"Error al insertar cita: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateCita(self, id_cita, id_disponibilidad_horaria, id_paciente, observacion, id_estado_cita):
        """Actualiza una cita y gestiona la disponibilidad horaria"""
        # Primero obtener la disponibilidad horaria anterior
        getDisponibilidadAnteriorSQL = """
        SELECT id_disponibilidad_horaria FROM citas WHERE id_cita = %s
        """
        updateCitaSQL = """
        UPDATE citas
        SET id_disponibilidad_horaria=%s, id_paciente=%s, observacion=%s, id_estado_cita=%s
        WHERE id_cita=%s
        """
        liberarDisponibilidadSQL = """
        UPDATE disponibilidad_horaria
        SET estado = TRUE
        WHERE id_disponibilidad_horaria = %s
        """
        ocuparDisponibilidadSQL = """
        UPDATE disponibilidad_horaria
        SET estado = FALSE
        WHERE id_disponibilidad_horaria = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            # 1. Obtener disponibilidad anterior
            cur.execute(getDisponibilidadAnteriorSQL, (id_cita,))
            resultado = cur.fetchone()
            if not resultado:
                return False
            
            id_disponibilidad_anterior = resultado[0]
            
            # 2. Si cambió la disponibilidad horaria
            if id_disponibilidad_anterior != id_disponibilidad_horaria:
                # Verificar que la nueva disponibilidad esté libre
                cur.execute("SELECT estado FROM disponibilidad_horaria WHERE id_disponibilidad_horaria = %s", 
                           (id_disponibilidad_horaria,))
                nueva_disponibilidad = cur.fetchone()
                
                if not nueva_disponibilidad or not nueva_disponibilidad[0]:
                    app.logger.error("La nueva disponibilidad no está disponible")
                    return False
                
                # Liberar la disponibilidad anterior
                cur.execute(liberarDisponibilidadSQL, (id_disponibilidad_anterior,))
                
                # Ocupar la nueva disponibilidad
                cur.execute(ocuparDisponibilidadSQL, (id_disponibilidad_horaria,))
            
            # 3. Actualizar la cita
            cur.execute(updateCitaSQL, (id_disponibilidad_horaria, id_paciente, observacion, id_estado_cita, id_cita))
            filas_afectadas = cur.rowcount
            
            con.commit()
            return filas_afectadas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar cita: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteCita(self, id_cita):
        """Elimina una cita y LIBERA la disponibilidad horaria"""
        # Primero obtener la disponibilidad horaria
        getDisponibilidadSQL = """
        SELECT id_disponibilidad_horaria FROM citas WHERE id_cita = %s
        """
        deleteCitaSQL = """
        DELETE FROM citas WHERE id_cita=%s
        """
        liberarDisponibilidadSQL = """
        UPDATE disponibilidad_horaria
        SET estado = TRUE
        WHERE id_disponibilidad_horaria = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            # 1. Obtener la disponibilidad horaria de la cita
            cur.execute(getDisponibilidadSQL, (id_cita,))
            resultado = cur.fetchone()
            
            if not resultado:
                return False
            
            id_disponibilidad_horaria = resultado[0]
            
            # 2. Eliminar la cita
            cur.execute(deleteCitaSQL, (id_cita,))
            rows_affected = cur.rowcount
            
            # 3. Liberar la disponibilidad horaria (marcar como disponible)
            if rows_affected > 0:
                cur.execute(liberarDisponibilidadSQL, (id_disponibilidad_horaria,))
            
            con.commit()
            return rows_affected > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar cita: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def getCitasByPaciente(self, id_paciente):
        """Obtiene todas las citas de un paciente específico"""
        citaSQL = """
        SELECT 
            c.id_cita,
            med.nombre AS medico_nombre,
            med.apellido AS medico_apellido,
            e.descripcion AS especialidad,
            dh.fecha,
            dh.hora_inicio,
            dh.hora_fin,
            c.observacion,
            ec.descripcion AS estado_cita
        FROM citas c
        INNER JOIN disponibilidad_horaria dh ON c.id_disponibilidad_horaria = dh.id_disponibilidad_horaria
        INNER JOIN agenda_medicas am ON dh.id_agenda_medica = am.id_agenda_medica
        INNER JOIN medicos m ON am.id_medico = m.id_medico
        INNER JOIN personas med ON m.id_persona = med.id_persona
        INNER JOIN especialidades e ON am.id_especialidad = e.id_especialidad
        INNER JOIN estado_citas ec ON c.id_estado_cita = ec.id_estado_cita
        WHERE c.id_paciente = %s
        ORDER BY dh.fecha DESC, dh.hora_inicio DESC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(citaSQL, (id_paciente,))
            citas = cur.fetchall()
            return [{
                'id_cita': cita[0],
                'medico_nombre': cita[1],
                'medico_apellido': cita[2],
                'especialidad': cita[3],
                'fecha': str(cita[4]),
                'hora_inicio': str(cita[5]),
                'hora_fin': str(cita[6]),
                'observacion': cita[7],
                'estado_cita': cita[8]
            } for cita in citas]
        except Exception as e:
            app.logger.error(f"Error al obtener citas del paciente: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()