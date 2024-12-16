import psycopg2

class Conexion:

    """Metodo constructor
    """
    def __init__(self):
        self.con = psycopg2.connect(dbname="agenda_medica_db", user="postgres", password="19092003", host="localhost", port=5432)
   
    """getConexion

        retorno la instancia de la base de datos

     """
   
    
    def getConexion(self):
        return self.con
