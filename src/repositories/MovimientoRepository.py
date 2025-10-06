from database.database import getConnection, returnConnection
from .InteraccionesRepository import InteraccionesRepository

class MovimientoRepository:
    """Clase encargada de traer los movimientos de la BD."""
    def __init__(self) -> None:
        pass
    def verUltimosMovimientos(self, pin:str)->tuple:
        """Consigue por el pin del usuario los últimos 5 movimientos ordenados por fecha_operación."""
        conexion = getConnection();
        cur = conexion.cursor()
        try:
            cur.execute("""
       SELECT m.importe, m.concepto, m.saldo_restante, m.fecha_operacion
        FROM Movimientos m
        WHERE m.id_cuenta = (
            SELECT c.id_cuenta
            FROM Cuenta c
            WHERE c.pin = crypt(%s, c.pin)
        )
        ORDER BY m.fecha_operacion DESC
        LIMIT 5;
       """, 
            (pin,))
            resultado = cur.fetchall()
            if resultado is not None:
                InteraccionesRepository().registrarInteraccion(pin,"Movimiento")
                return resultado
            else:
                return None
        except Exception as e:
            return e
        finally:
            cur.close()
            returnConnection(conexion)

            