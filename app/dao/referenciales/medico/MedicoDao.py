from flask import current_app as app
from app.conexion.Conexion import Conexion

class MedicoDao:

    def getMedicos(self):
        medicoSQL = """
      SELECT
        m.id_medico, p.nombre, p.apellido, m.matricula, e.descripcion
            FROM medicos m, personas p, estado_laborales e
            where m.id_persona=p.id_persona and m.id_estado_laboral=e.id_estado_laboral
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(medicoSQL)
            medicos = cur.fetchall()

            # Transformar los datos en una lista de diccionarios con los nuevos campos
            return [{'id_medico': medico[0], 'nombre': medico[1], 'apellido': medico[2],'matricula': medico[3],'estado_laboral': medico[4]} for medico in medicos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los medicos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getMedicoById(self, id_medico):
        medicoSQL = """
         SELECT
            m.id_medico, p.nombre, p.apellido, m.matricula, e.descripcion, p.id_persona, e.id_estado_laboral
            FROM medicos m, personas p, estado_laborales e
            Where m.id_persona=p.id_persona and m.id_estado_laboral=e.id_estado_laboral and m.id_medico=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(medicoSQL, (id_medico,))
            medicoEncontrado = cur.fetchone()
            if medicoEncontrado:
                return {
                    "id_medico": medicoEncontrado[0],
                    "nombre": medicoEncontrado[1],
                    "apellido": medicoEncontrado[2],
                    "matricula": medicoEncontrado[3],
                    "descripcion": medicoEncontrado[4],
                    "id_persona": medicoEncontrado[5],
                    "id_estado_laboral": medicoEncontrado[6]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener medico por ID: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarMedico(self, id_persona,matricula,id_estado_laboral):
        insertMedicoSQL = """
        INSERT INTO medicos(id_estado_laboral,matricula, id_persona) VALUES(%s, %s,%s) RETURNING id_medico
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertMedicoSQL, (id_estado_laboral,matricula, id_persona))
            medico_id = cur.fetchone()[0]
            con.commit()
            return medico_id

        except Exception as e:
            app.logger.error(f"Error al insertar medico: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateMedico(self, id_medico, id_persona, matricula,id_estado_laboral):
        updateMedicoSQL = """
        UPDATE medicos
        SET  matricula=%s, id_persona=%s, id_estado_laboral=%s
        WHERE id_medico=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateMedicoSQL, (matricula,id_persona,id_estado_laboral, id_medico))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar medico: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteMedico(self, id_medico):
        deleteMedicoSQL = """
        DELETE FROM medicos
        WHERE id_medico=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteMedicoSQL, (id_medico,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar medico: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
