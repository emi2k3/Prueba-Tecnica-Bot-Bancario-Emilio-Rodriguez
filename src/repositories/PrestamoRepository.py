from database.database import getConnection, returnConnection
from .InteraccionesRepository import InteraccionesRepository

class PrestamoRepository:
    """Trae prestamos pendientes, y cuotas no pagas. Además inserta nuevos prestamos y cuotas."""
    def __init__(self) -> None:
        pass
    def verPrestamosPendientes(self, pin:str)->tuple:
        """Trae todos los prestamos pendientes del usuario."""
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
                InteraccionesRepository().registrarInteraccion(pin,"Prestamo")
                return resultado
            else:
                return []
        except Exception as e:
            return e
        finally:
            cur.close()
            returnConnection(conexion)

    def verCuotasRestantesPrestamo(self, id_prestamo:int,pin:str)->tuple:
        """Trae todas las cuotas restantes de un id_prestamo."""
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
                InteraccionesRepository().registrarInteraccion(pin,"Prestamo")
                return resultado
            else:
                return []
        except Exception as e:
            return e
        finally:
            cur.close()
            returnConnection(conexion)
    
    def insertarPrestamo(self, pin:str,monto_original:int,tasa_interes:float,cuota_mensual:float,plazo_meses:int) -> bool:
        """Inserta un nuevo prestamo, y por cada cada plazo_mes se inserta una nueva cuota en cuota_prestamo."""
        conexion = getConnection();
        cur = conexion.cursor()
        try: 
            cur.execute("""
            INSERT INTO Prestamo (monto_original, tasa_interes, cuota_mensual, plazo_meses, id_cuenta)
            SELECT %s, %s, %s, %s, c.id_cuenta
            FROM Cuenta c
            WHERE c.pin = crypt(%s, c.pin)
            RETURNING id_prestamo, fecha_otorgamiento;
        """, (monto_original, tasa_interes, cuota_mensual, plazo_meses, pin))
            row = cur.fetchone()
            if not row:
                conexion.rollback()
                return False

            id_prestamo, fecha_otorgamiento = row

         
            cur.execute("""
            SELECT insertCuotas(%s, %s, %s, %s);
        """, (id_prestamo, cuota_mensual, plazo_meses, fecha_otorgamiento))

            conexion.commit()
            InteraccionesRepository().registrarInteraccion(pin,"Prestamo")
            return True
        except Exception as e:
            conexion.rollback()
            return e
        finally:
            cur.close()
            returnConnection(conexion)

    def isMoroso(self, id_prestamo:int)->bool:
        """Busca si el usuario tiene cuotas sin pagar en un prestamo."""
        try:
            conexion = getConnection();
            cur = conexion.cursor()
            cur.execute("""
        SELECT 1
        FROM Cuota_Prestamo
        WHERE id_prestamo = %s
          AND pagada = FALSE 
          AND NOW()>fecha_vencimiento
        LIMIT 1;
    """, (id_prestamo,))
       
            resultado = cur.fetchone()
            if not resultado:
                #No lo hace el usuario, lo hace la ia.
                return False
            else:
                return True
        except Exception as e:
            return e
        finally:
            cur.close()
            returnConnection(conexion)