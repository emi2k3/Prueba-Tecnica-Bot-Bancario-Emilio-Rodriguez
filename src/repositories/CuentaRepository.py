from psycopg2.extensions import cursor
from database.database import getConnection, returnConnection

class CuentaRepository:

    def __init__(self) -> None:
        pass
    #Conseguir del usuario que esta autenticado un id
    def consultarSaldo(self, pin:str)->int:

        conexion = getConnection();
        cur = conexion.cursor()
        cur.execute('SELECT saldo from usuario WHERE ')
        try:
            saldo = cur.fetchone()[0]
            if saldo is not None:
                return saldo
            else:
                raise RuntimeError("Hubo un error al solicitar el saldo")
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