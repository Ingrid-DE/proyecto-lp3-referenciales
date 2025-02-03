# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class Agenda_medicaDao:

    def getAgenda_medicas(self):
        agenda_medicaSQL = """
        SELECT 
            a.id_agenda_medica, p.nombre, p.apellido, e.descripcion, t.descripcion, s.nombre, es.descripcion
                FROM agenda_medicas a, personas p, especialidades e, turnos t, sala_atenciones s, estado_laborales es
                where a.id_persona=p.id_persona and a.id_especialidad=e.id_especialidad and a.id_turno=t.id_turno and a.id_sala_atencion=s.id_sala_atencion and a.id_estado_laboral=es.id_estado_laboral
            """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(agenda_medicaSQL)
            agenda_medicas = cur.fetchall()
            return [{
                'id_agenda_medica':  agenda_medica[0], 'nombre':  agenda_medica[1], 'apellido':  agenda_medica[2], 'especialidad':  agenda_medica[3],  'turno':  agenda_medica[4], 'sala_atencion': agenda_medica[5], 'estado_laboral': agenda_medica[6]} for agenda_medica in agenda_medicas]
        
        except Exception as e:
            app.logger.error(f"Error al obtener todas las agendas médicas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getAgenda_medicaById(self, id_agenda_medica):
        agenda_medicaSQL = """
        SELECT 
            a.id_agenda_medica, p.nombre, p.apellido, e.descripcion, t.descripcion, s.nombre, es.descripcion, p.id_persona, e.id_especialidad, t.id_turno, s.id_sala_atencion, es.id_estado_laboral
            FROM agenda_medicas a, personas p, especialidades e, turnos t, sala_atenciones s, estado_laborales es
            WHERE a.id_persona=p.id_persona and a.id_especialidad=e.id_especialidad and a.id_turno=t.id_turno and a.id_sala_atencion=s.id_sala_atencion and a.id_estado_laboral=es.id_estado_laboral and a.id_agenda_medica=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(agenda_medicaSQL, (id_agenda_medica,))
            agenda_medicaEncontrada = cur.fetchone()
            if agenda_medicaEncontrada:
                return {
                    "id_agenda_medica": agenda_medicaEncontrada[0],
                    "nombre": agenda_medicaEncontrada[1],
                    "apellido": agenda_medicaEncontrada[2],
                    "especialidad": agenda_medicaEncontrada[3],
                    "turno": agenda_medicaEncontrada[4],
                    "sala_atencion": agenda_medicaEncontrada[5],
                    "estado_laboral": agenda_medicaEncontrada[6],
                    "id_persona": agenda_medicaEncontrada[7],
                    "id_especialidad": agenda_medicaEncontrada[8],
                    "id_turno": agenda_medicaEncontrada[9],
                    "id_sala_atencion": agenda_medicaEncontrada[10],
                    "id_estado_laboral": agenda_medicaEncontrada[11]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener agenda médica: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def guardarAgenda_medica(self, id_persona, id_especialidad, id_turno, id_sala_atencion, id_estado_laboral,):
        insertAgenda_medicaSQL = """
        INSERT INTO agenda_medicas(id_persona, id_especialidad, id_turno, id_sala_atencion, id_estado_laboral) VALUES(%s, %s, %s, %s,%s) RETURNING id_agenda_medica
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(insertAgenda_medicaSQL, (id_persona, id_especialidad, id_turno, id_sala_atencion, id_estado_laboral))
            agenda_medica_id = cur.fetchone()[0]
            con.commit()
            return agenda_medica_id
        except Exception as e:
            app.logger.error(f"Error al insertar agenda médica: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateAgenda_medica(self, id_agenda_medica, id_persona, id_especialidad,  id_turno, id_sala_atencion, id_estado_laboral):
        updateAgenda_medicaSQL = """
        UPDATE agenda_medicas
        SET id_persona=%s, id_especialidad=%s, id_turno=%s, id_sala_atencion=%s, id_estado_laboral=%s
        WHERE id_agenda_medica=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(updateAgenda_medicaSQL, ( id_persona, id_especialidad, id_turno, id_sala_atencion, id_estado_laboral, id_agenda_medica))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar agenda médica: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteAgenda_medica(self, id_agenda_medica):
        deleteAgenda_medicaSQL = """
        DELETE FROM agenda_medicas
        WHERE id_agenda_medica=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(deleteAgenda_medicaSQL, (id_agenda_medica,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar agenda médica: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
