from psycopg2.extensions import cursor
from database.database import getConnection, returnConnection

class MovimientoRepository:

    def __init__(self) -> None:
        pass
    def verUltimosMovimientos(self, pin:str)->int:
        conexion = getConnection();
        cur = conexion.cursor()
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
        try:
            resultado = cur.fetchall()
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

            