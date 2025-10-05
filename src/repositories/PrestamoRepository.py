from psycopg2.extensions import cursor
from database.database import getConnection, returnConnection

class PrestamoRepository:

    def __init__(self) -> None:
        pass
    def verPrestamosPendientes(self, pin:str)->int:
        conexion = getConnection();
        cur = conexion.cursor()
        cur.execute("""
      SELECT p.id_prestamo,
               p.monto_original,
               p.tasa_interes,
               p.cuota_mensual,
               p.plazo_meses,
               p.fecha_otorgamiento
        FROM Prestamo p
        WHERE p.id_cuenta = (
            SELECT c.id_cuenta
            FROM Cuenta c
            WHERE c.pin = crypt(%s, c.pin)
        )
        AND EXISTS (
            SELECT 1 FROM Cuota_Prestamo cu
            WHERE cu.id_prestamo = p.id_prestamo
            AND cu.pagada = FALSE
        );
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
    def verCuotasRestantesPrestamo(self, id_prestamo:int)->int:
        conexion = getConnection();
        cur = conexion.cursor()
        cur.execute("""
        SELECT numero_cuota, monto_cuota, fecha_vencimiento
        FROM Cuota_Prestamo
        WHERE id_prestamo = %s
          AND pagada = FALSE
        ORDER BY numero_cuota;
    """, (id_prestamo,))
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


            