import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from repositories.CuentaRepository import CuentaRepository
from repositories.InteraccionesRepository import InteraccionesRepository
class CuentaService:
    def __init__(self) -> None:
        pass
    def consultarSaldo(self, pin: str) -> int:
        """Consulta el el saldo del usuario utilizando el pin. Llama a CuentaRepository."""
        try:
            saldo = CuentaRepository().consultarSaldo(pin)
            return saldo
        except Exception as e:
            return e
    def LogIn(self, pin:str)->bool:
        """Utiliza el pin para iniciar sesión. Llama a CuentaRepository."""
        try:
            valido = pin.isdigit()
            if not valido:
                return False
            return CuentaRepository().LogIn(pin)
        except Exception as e:
            return e
        #Suponiendo que la inflación es algo fijo y sube SOLO un 2.35%
    def plazofijo(self, pin: str,dias:int,monto:int) -> bool:
        """Calcula si le conviene el plazo fijo al usuario."""
        inflacion_esperada = 2.35/100
        tna = 0
    # Tasas Efectivas Anuales.
        if 181 <= dias <= 366:
            tna = 1.60 / 100 
        elif 367 <= dias <= 546:
            tna = 2.10 / 100 
        elif 547 <= dias <= 731:
            tna = 2.30 / 100 
        elif 732 <= dias <= 1096:
            tna = 2.60 / 100 
        else:
            return 0

    # Perdida por inflación
        inflacion_proporcional = (inflacion_esperada / 365) * dias
    # Ganancia
        tasa_real_proporcional = ((tna / 365) * dias) - inflacion_proporcional
    
        ganancia_neta_en_dinero = monto * tasa_real_proporcional
        InteraccionesRepository().registrarInteraccion(pin,"Consulta")
        return ganancia_neta_en_dinero > 0