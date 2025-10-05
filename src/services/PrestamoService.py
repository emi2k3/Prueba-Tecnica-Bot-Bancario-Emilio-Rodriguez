from decimal import Decimal
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import json

from repositories.PrestamoRepository import PrestamoRepository
class PrestamoService:
    def __init__(self) -> None:
        pass
    def consultarPrestamos(self, pin:str):
        pendientes = PrestamoRepository().verPrestamosPendientes(pin)
        pendientes_map = list(map(lambda t: {
    "id_prestamo": t[0],
    "monto_original": t[1],
    "tasa_interes": str(t[2]),
    "cuota_mensual": t[3],
    "plazo_meses": t[4],
    "fecha_otorgamiento": t[5].strftime("%Y-%m-%d"),
}, pendientes))
        return pendientes_map

       
    def consultarCuotasdeUnPrestamo(self, id_prestamo:int):
        pendientes = PrestamoRepository().verCuotasRestantesPrestamo(id_prestamo)
        pendientes_map = list(map(lambda t: {
    "numero_cuota": t[0],
    "monto_cuota": t[1],
    "fecha_vencimiento": t[2].strftime("%Y-%m-%d"),
}, pendientes))
        return pendientes_map
    def pedirPrestamo(self, pin:str,monto:int,cuotas:int):
        pass
