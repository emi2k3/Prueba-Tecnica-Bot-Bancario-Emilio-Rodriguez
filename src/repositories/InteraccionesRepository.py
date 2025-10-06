from database.database import getConnection, returnConnection

class InteraccionesRepository:

    def __init__(self) -> None:
        pass
    def registrarInteraccion(self, pin:str,tipo:str):
        """Registra todas las interacciones del usuario."""

        conexion = getConnection();
        cur = conexion.cursor()
        try:
            cur.execute("""
        INSERT INTO Interacciones (fecha_hora, tipo, id_cuenta)
        VALUES (NOW(),%s,(SELECT id_cuenta FROM Cuenta WHERE pin=crypt(%s,pin) LIMIT 1));""", 
            (tipo,pin))
        
        except Exception as e:
            return e
        finally:
            cur.close()
            returnConnection(conexion)


            