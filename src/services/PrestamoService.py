from decimal import Decimal
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import json

from repositories.PrestamoRepository import PrestamoRepository


class PrestamoService:
    def __init__(self) -> None:
        pass
    def consultarPrestamos(self, pin:str)->list:
        """Llama a prestamo respository pidiendo los prestamos pendientes y luego sanitiza los datos obtenídos para el bot."""
        try:
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
        except Exception as e:
            return e
       
    def consultarCuotasdeUnPrestamo(self, id_prestamo:int,pin:str):
        """Llama a prestamo respository pidiendo las cuotas de un prestamo y luego sanitiza los datos obtenídos para el bot."""    
        pendientes = PrestamoRepository().verCuotasRestantesPrestamo(id_prestamo,pin)
        pendientes_map = list(map(lambda t: {
    "numero_cuota": t[0],
    "monto_cuota": t[1],
    "fecha_vencimiento": t[2].strftime("%Y-%m-%d"),
}, pendientes))
        return pendientes_map

    def interesTotal(self,monto:int,cuotas:int,pin:str):
        """Calcula el monto total a pagar con intereses"""
        tasa_mensual = self.calcularTasa(cuotas,self.isMoroso(pin))
        tasa_mensual
        C = (float(monto) * tasa_mensual) / (1 - (1 + tasa_mensual) ** - float(cuotas))
        return  round(C * cuotas,2) 


    def calcularTasa(self,cuotas:int,mora:bool)->float:
        """Calcula la tasa de intereses,según las cuotas y si es moroso."""
        tasa_anual=0
        if cuotas >=2 and cuotas<=6:
            tasa_anual= 0.27
        elif cuotas >=7 and cuotas<=12:
            tasa_anual= 0.30
        elif cuotas >=13 and cuotas<=24:
            tasa_anual= 0.31
        elif cuotas >=25 and cuotas<=36:
            tasa_anual= 0.32
        if mora:
            tasa_mensual = min(tasa_anual + 0.15, 0.45)/12
        else:
            tasa_mensual = tasa_anual / 12
        return tasa_mensual

    
    def pedirPrestamo(self, pin:str,monto_original: int, plazo_meses: int)->bool:
        """Llama al repository para que inserte un nuevo prestamo."""
        try:
            pendientes = PrestamoRepository().verPrestamosPendientes(pin)
            if(len(pendientes)>=2):
                return False
            else:
                es_moroso = self.isMoroso(pin)
                tasa_interes = self.calcularTasa(plazo_meses, es_moroso)
                cuota_mensual = self.interesTotal(monto_original, plazo_meses, pin) / plazo_meses
                
                resultado = PrestamoRepository().insertarPrestamo(pin, monto_original, tasa_interes, cuota_mensual, plazo_meses)
                return resultado
        except:
            return False

    def isMoroso(self,pin:str)->bool:
        """Llama al repository para conseguir si el usuario es moroso o no."""
        pendientes = PrestamoRepository().verPrestamosPendientes(pin)
        if not pendientes:
            return False
        for prestamo in pendientes: 
            id_prestamo = prestamo[0] 
            mora = PrestamoRepository().isMoroso(id_prestamo) 
            if mora:
                return True     
        return False  
