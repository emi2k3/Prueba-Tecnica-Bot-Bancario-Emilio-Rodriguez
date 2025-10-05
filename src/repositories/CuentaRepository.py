from psycopg2.extensions import cursor
from database.database import getConnection, returnConnection

class CuentaRepository:

    def __init__(self) -> None:
        pass
    #Conseguir del usuario que esta autenticado un id
    def consultarSaldo(self, pin:str)->int:
        conexion = getConnection();
        cur = conexion.cursor()
        cur.execute("""
        SELECT saldo FROM Cuenta
        WHERE pin=crypt(%s,pin);""", 
            (pin,))
        try:
            resultado = cur.fetchone()
            if resultado is not None:
                return resultado
            else:
                return None
        except Exception as e:
            print(e)
            return None
        finally:
            cur.close()
            returnConnection(conexion)

    def LogIn(self, pin:str)->bool:
        conexion = getConnection();
        cur = conexion.cursor()
        cur.execute("""
        SELECT * FROM Cuenta
        WHERE pin=crypt(%s,pin);""", 
            (pin,))
        try:
            resultado = cur.fetchone()
            if resultado is not None:
                return True
            else:
                return False
        finally:
            cur.close()
            returnConnection(conexion)

            