import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from repositories.MovimientoRepository import MovimientoRepository
class MovimientoService:
    """Clase encargada de manejar los datos que trae Repository y el usuario para los movimientos."""
    def __init__(self) -> None:
        pass
    def verUltimosMovimientos(self, pin: str) -> []:
        """Retorna los últimos 5 movimientos del usuario, utiliza el pin para identificarlo. Llama a Movimiento Repository."""
        try:
            transacciones_consulta = MovimientoRepository().verUltimosMovimientos(pin)
            transacciones_map = list(map(lambda t: {
    "importe": t[0],
    "concepto": t[1],
    "saldo_restante": t[2],
    "fecha_operacion": t[3].strftime("%Y-%m-%d %H:%M:%S")
}, transacciones_consulta))
            return transacciones_map
        except Exception as e:
            return e
            


