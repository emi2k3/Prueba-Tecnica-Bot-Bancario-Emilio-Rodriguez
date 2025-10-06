from sys import excepthook
from database.database import getConnection, returnConnection
from .InteraccionesRepository import InteraccionesRepository
class CuentaRepository:

    def __init__(self) -> None:
        pass
    def consultarSaldo(self, pin:str)->int:
        """Consigue el saldo del usuario por su pin."""

        conexion = getConnection();
        cur = conexion.cursor()
        try:
            cur.execute("""
        SELECT saldo FROM Cuenta
        WHERE pin=crypt(%s,pin);""", 
            (pin,))
     
            resultado = cur.fetchone()
            if resultado is not None:
                InteraccionesRepository().registrarInteraccion(pin,"Consulta")
                return resultado
            else:
                return 0
        except Exception as e:
            return e
        finally:
            cur.close()
            returnConnection(conexion)

    def LogIn(self, pin:str)->bool:
        """Inicia sesión del usuario buscandolo en la BD por su pin."""
        
        conexion = getConnection();
        cur = conexion.cursor()
        try:
            cur.execute("""
        SELECT * FROM Cuenta
        WHERE pin=crypt(%s,pin);""", 
            (pin,))
      
            resultado = cur.fetchone()
            if resultado is not None:
                InteraccionesRepository().registrarInteraccion(pin,"Consulta")
                return True
            else:
                return False
        except Exception as e:
            return e
        finally:
            cur.close()
            returnConnection(conexion)

            