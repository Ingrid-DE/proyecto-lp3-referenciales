# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class EnfermedadDao:

    def getEnfermedad(self):              

        enfermedadSQL = """
        SELECT id, descripcion
        FROM enfermedades
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(enfermedadSQL)
            enfermedades = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': enfermedad[0], 'descripcion': enfermedad[1]} for enfermedad in enfermedades]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las enfermedades: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getEnfermedadById(self, id):

        enfermedadSQL = """
        SELECT id, descripcion
        FROM enfermedades WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(enfermedadSQL, (id,))
            enfermedadEncontrada = cur.fetchone() # Obtener una sola fila
            if enfermedadEncontrada:
                return {
                        "id": enfermedadEncontrada[0],
                        "descripcion": enfermedadEncontrada[1]
                    }  # Retornar los datos de la ciudad
            else:
                return None # Retornar None si no se encuentra la ciudad
        except Exception as e:
            app.logger.error(f"Error al obtener enfermedad: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarEnfermedad(self, descripcion):

        insertEnfermedadSQL = """
   INSERT INTO enfermedades(descripcion) VALUES(%s) RETURNING id        
   """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertEnfermedadSQL, (descripcion,))
            enfermedad_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return enfermedad_id
        
        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar enfermedad: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

          # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateEnfermedad(self, id, descripcion):

        updateEnfermedadSQL = """
        UPDATE enfermedades
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateEnfermedadSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas            con.commit()
            con.commit()
        
            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar enfermedad: {str(e)}")
            con.rollback()
            return False 
               
        finally:
            cur.close()
            con.close()

    def deleteEnfermedad(self, id):

        updateEnfermedadSQL = """
        DELETE FROM enfermedades
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(updateEnfermedadSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila        
        except Exception as e:
            app.logger.error(f"Error al eliminar enfermedad: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
