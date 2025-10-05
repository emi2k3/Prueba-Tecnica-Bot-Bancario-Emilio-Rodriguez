import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from repositories.CuentaRepository import CuentaRepository
class CuentaService:
    def __init__(self) -> None:
        pass
    def consultarSaldo(self, pin: str) -> int:
        saldo = CuentaRepository().consultarSaldo(pin)
        return saldo
    def LogIn(self, pin:str)->bool:
        valido = pin.isdigit()
        if not valido:
            return False
        return CuentaRepository().LogIn(pin)

