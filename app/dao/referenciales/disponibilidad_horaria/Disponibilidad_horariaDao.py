from flask import current_app as app
from app.conexion.Conexion import Conexion

class Disponibilidad_horariaDao:

    def __init__(self):
        self.conexion = Conexion()

    # Trae todas las disponibilidades con info de agenda, medico, etc.
    def getDisponibilidades(self):
        try:
            conn = self.conexion.getConexion()
            cursor = conn.cursor()

            sql = """
                SELECT dh.id_disponibilidad_horaria,
                       dh.fecha,
                       dh.hora_inicio,
                       dh.hora_fin,
                       dh.estado,
                       am.id_agenda_medica,
                       p.nombre || ' ' || p.apellido AS medico,
                       e.descripcion AS especialidad,
                       d.descripcion AS dia,
                       t.descripcion AS turno,
                       s.nombre AS sala,
                       el.descripcion AS estado_laboral
                FROM disponibilidad_horaria dh
                JOIN agenda_medicas am ON dh.id_agenda_medica = am.id_agenda_medica
                JOIN medicos m ON am.id_medico = m.id_medico
                JOIN personas p ON m.id_persona = p.id_persona
                JOIN especialidades e ON am.id_especialidad = e.id_especialidad
                JOIN dias d ON am.id_dia = d.id_dia
                JOIN turnos t ON am.id_turno = t.id_turno
                JOIN sala_atenciones s ON am.id_sala_atencion = s.id_sala_atencion
                JOIN estado_laborales el ON am.id_estado_laboral = el.id_estado_laboral
                ORDER BY dh.fecha, dh.hora_inicio;
            """
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            app.logger.error(f"Error en getDisponibilidades: {e}")
            return None

    # Trae disponibilidad por ID CON INFO DE AGENDA para el formulario de edición
    def getDisponibilidadById(self, id_disponibilidad):
        try:
            conn = self.conexion.getConexion()
            cursor = conn.cursor()

            sql = """
                SELECT dh.id_disponibilidad_horaria,
                       dh.id_agenda_medica,
                       dh.fecha,
                       dh.hora_inicio,
                       dh.hora_fin,
                       dh.estado,
                       p.nombre || ' ' || p.apellido || ' - ' || 
                       e.descripcion || ' - ' || 
                       d.descripcion || ' - ' || 
                       t.descripcion || ' - ' || 
                       s.nombre AS agenda_medica
                FROM disponibilidad_horaria dh
                JOIN agenda_medicas am ON dh.id_agenda_medica = am.id_agenda_medica
                JOIN medicos m ON am.id_medico = m.id_medico
                JOIN personas p ON m.id_persona = p.id_persona
                JOIN especialidades e ON am.id_especialidad = e.id_especialidad
                JOIN dias d ON am.id_dia = d.id_dia
                JOIN turnos t ON am.id_turno = t.id_turno
                JOIN sala_atenciones s ON am.id_sala_atencion = s.id_sala_atencion
                WHERE dh.id_disponibilidad_horaria = %s;
            """
            cursor.execute(sql, (id_disponibilidad,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            app.logger.error(f"Error en getDisponibilidadById: {e}")
            return None

    # Trae disponibilidades filtradas por agenda (y opcionalmente por fecha)
    def getDisponibilidadesPorAgenda(self, agenda_id, fecha=None):
        try:
            conn = self.conexion.getConexion()
            cursor = conn.cursor()

            sql = """
                SELECT id_disponibilidad_horaria, id_agenda_medica, fecha, hora_inicio, hora_fin, estado
                FROM disponibilidad_horaria
                WHERE id_agenda_medica = %s
            """
            params = [agenda_id]

            if fecha:
                sql += " AND fecha = %s"
                params.append(fecha)

            sql += " ORDER BY fecha, hora_inicio"

            cursor.execute(sql, tuple(params))
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            app.logger.error(f"Error en getDisponibilidadesPorAgenda: {e}")
            return None

    # Inserta nueva disponibilidad
    def addDisponibilidad(self, data):
        try:
            conn = self.conexion.getConexion()
            cursor = conn.cursor()

            sql = """
                INSERT INTO disponibilidad_horaria (id_agenda_medica, fecha, hora_inicio, hora_fin, estado)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_disponibilidad_horaria;
            """
            values = (
                data.get("id_agenda_medica"),
                data.get("fecha"),
                data.get("hora_inicio"),
                data.get("hora_fin"),
                data.get("estado", True)
            )

            cursor.execute(sql, values)
            id_insertado = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            return {
                "id_disponibilidad_horaria": id_insertado,
                **data
            }
        except Exception as e:
            app.logger.error(f"Error en addDisponibilidad: {e}")
            conn.rollback()
            return None

    # Actualiza una disponibilidad
    def updateDisponibilidad(self, id_disponibilidad, data):
        try:
            conn = self.conexion.getConexion()
            cursor = conn.cursor()

            sql = """
                UPDATE disponibilidad_horaria
                SET id_agenda_medica = %s,
                    fecha = %s,
                    hora_inicio = %s,
                    hora_fin = %s,
                    estado = %s
                WHERE id_disponibilidad_horaria = %s
                RETURNING id_disponibilidad_horaria;
            """
            values = (
                data.get("id_agenda_medica"),
                data.get("fecha"),
                data.get("hora_inicio"),
                data.get("hora_fin"),
                data.get("estado", True),
                id_disponibilidad
            )

            cursor.execute(sql, values)
            result = cursor.fetchone()
            
            if result:
                conn.commit()
                cursor.close()
                conn.close()
                return {
                    "id_disponibilidad_horaria": result[0],
                    **data
                }
            else:
                cursor.close()
                conn.close()
                return None
                
        except Exception as e:
            app.logger.error(f"Error en updateDisponibilidad: {e}")
            conn.rollback()
            return None

    # Elimina una disponibilidad
    def deleteDisponibilidad(self, id_disponibilidad):
        try:
            conn = self.conexion.getConexion()
            cursor = conn.cursor()

            sql = """
                DELETE FROM disponibilidad_horaria
                WHERE id_disponibilidad_horaria = %s
                RETURNING id_disponibilidad_horaria;
            """
            cursor.execute(sql, (id_disponibilidad,))
            result = cursor.fetchone()
            
            if result:
                conn.commit()
                cursor.close()
                conn.close()
                return True
            else:
                cursor.close()
                conn.close()
                return False
                
        except Exception as e:
            app.logger.error(f"Error en deleteDisponibilidad: {e}")
            conn.rollback()
            return False