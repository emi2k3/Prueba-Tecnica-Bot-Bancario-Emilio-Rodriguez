import os
from mistralai import Mistral
from dotenv import load_dotenv
import json

from services.PrestamoService import PrestamoService
from services.CuentaService import CuentaService
from services.MovimientoService import MovimientoService  

load_dotenv()
cuenta_service = CuentaService()  
movimiento_service = MovimientoService()  
prestamo_service = PrestamoService()

class MistralService:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.model = "mistral-large-latest"
        self.client = Mistral(api_key=self.api_key)
        #Cuenta
        def consultar_saldo(pin):
            return cuenta_service.consultarSaldo(pin)  
        #Movimientos
        def verUltimosMovimientos(pin):
            return movimiento_service.verUltimosMovimientos(pin)  
        #Prestamos
        def consultarPrestamos(pin):
            return prestamo_service.consultarPrestamos(pin)  
        def consultarCuotasdeUnPrestamo(fecha_prestamo, pin=None):
            prestamos = prestamo_service.consultarPrestamos(pin)
    # Buscar el préstamo que coincide con la fecha
            prestamo = next((p for p in prestamos if p["fecha_otorgamiento"] == fecha_prestamo), None)
            if not prestamo:
                return {"mensaje": "No se encontró un préstamo con esa fecha o ya está pagado."}
            return prestamo_service.consultarCuotasdeUnPrestamo(prestamo["id_prestamo"])   
        self.names_to_functions = {
            'consultarSaldo': consultar_saldo,
            'verUltimosMovimientos': verUltimosMovimientos,
            'consultarPrestamos': consultarPrestamos,
            'consultarCuotasdeUnPrestamo': consultarCuotasdeUnPrestamo
        }
        self.tools = [
    {
        "type": "function",
        "function": {
            "name": "consultarSaldo",
            "description": "Consulta el saldo actual del usuario. Llama esta tool directamente si el usuario pregunta por su saldo o cuánto tiene en su cuenta. No requiere parámetros, ya que usa el contexto interno (como el PIN). Después de recibir los datos, incluye el saldo en tu respuesta de forma amigable y pregunta '¿Qué más necesitas?'",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "verUltimosMovimientos",
            "description": "Obtiene los últimos movimientos del usuario. Llama esta tool directamente si el usuario confirma que quiere ver sus últimos movimientos. No requiere parámetros, ya que usa el contexto interno (PIN). Los datos ya vienen formateados; incorpóralos directamente en tu respuesta sin modificaciones extras (no agregues asteriscos ni markup). Termina preguntando '¿Qué más necesitas?'",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultarPrestamos",
            "description": "Obtiene todos los préstamos pendientes del usuario. Llama esta tool solo si el usuario confirma que quiere consultar sus préstamos pendientes. No requiere parámetros, ya que usa el contexto interno (PIN). No muestres 'id_prestamo'. Si no hay préstamos, no llames esta tool y responde: 'No tienes préstamos pendientes en este momento.' Después de recibir datos, lista los préstamos de forma clara (e.g., monto, fecha de otorgamiento) y pregunta '¿Quieres ver las cuotas de algún préstamo específico? Indícame la fecha.'",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultarCuotasdeUnPrestamo",
            "description": "Obtiene las cuotas pendientes de un préstamo específico. Llama esta tool solo después de haber llamado 'consultarPrestamos' o si el usuario proporciona la fecha del préstamo. Requiere la fecha en formato YYYY-MM-DD (conviértela si el usuario la da naturalmente). Si no hay cuotas pendientes, responde: 'Este préstamo ya está pagado.' Si hay, lista las cuotas de forma clara y termina preguntando '¿Qué más necesitas?'",
            "parameters": {
                "type": "object",
                "properties": {
                    "fecha_prestamo": {
                        "type": "string",
                        "description": "Fecha del préstamo en formato YYYY-MM-DD. Usa el historial de mensajes para obtenerla si ya se mencionó."
                    }
                },
                "required": ["fecha_prestamo"]
            }
        }
    }
]
    
    def procesar_mensaje(self, mensaje_usuario, historial_mensajes=None, pin=None):
        messages = []
        
        messages.append({
            "role": "system",
            "content": """
            Eres un bot bancario de Telegram para el Bank of Uruguay, un banco uruguayo. Responde de manera amigable, concisa y útil, como un asistente personal. Siempre usa las tools disponibles para consultar datos reales; no inventes información. 

Instrucciones clave:
- No saludes ni digas 'Hola', ya que el usuario ya inició sesión.
- Si el usuario menciona 'movimientos' sin especificar, pregunta: '¿Quieres ver tus últimos movimientos? Confírmame para consultar.' Y no agregues nada más en esa respuesta.
- Si menciona 'préstamos' sin especificar, pregunta: '¿Quieres consultar tus préstamos pendientes? Confírmame para proceder.' Y no agregues nada más.
- Para otras consultas, responde directamente usando la tool apropiada.
- Después de entregar datos de una tool, resume brevemente si es necesario y siempre termina preguntando: '¿Qué más necesitas?'
- Si no hay datos (e.g., no hay préstamos), informa amigablemente: 'No tienes préstamos pendientes en este momento.' Sin llamar tools innecesarias.
- Maneja fechas naturalmente: convierte formatos como '2 de septiembre de 2023' a 'YYYY-MM-DD' antes de pasar a tools.
- No muestres IDs internos como 'id_prestamo'. Formatea respuestas limpias, sin asteriscos ni markup extra.
- Si el usuario pregunta algo no cubierto por las tools, di: 'Lo siento, solo puedo ayudarte con saldo, movimientos y préstamos por ahora.'
- Cuando entregues listas de datos (como cuotas o movimientos), usa tablas Markdown para organizar: columnas claras (e.g., 'Cuota', 'Monto', 'Vencimiento'). Resalta la próxima cuota en negrita. Evita asteriscos o markup extra que no ayude. Si los montos son fijos, menciónalo una vez al inicio para no repetir.
- Mantén respuestas cortas: resume si la lista es larga (e.g., muestra solo las próximas 5 cuotas y ofrece ver más si el usuario pide). Siempre termina con una pregunta abierta como '¿Quieres pagar una cuota, ver detalles o algo más?' para guiar el flujo.
           
Instrucciones adicionales para formateo:
- Siempre usa texto plano en las respuestas. NO uses Markdown como **negrita**, *cursiva*, ni listas con asteriscos (*) a menos que sea para tablas (usa | para columnas).
            """
        })
        
        if historial_mensajes:
            messages.extend(historial_mensajes)
        
        messages.append({
            "role": "user",
            "content": mensaje_usuario
        })
        
        try:
       
            response = self.client.chat.complete(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
                parallel_tool_calls=False,
            )
            assistant_message = response.choices[0].message
            
            tool_calls = assistant_message.tool_calls or []
            content = assistant_message.content or ""  
            
      
            if tool_calls:
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_params = json.loads(tool_call.function.arguments)
                    
                   
                    messages.append({
                        "role": "assistant",
                        "content": content,
                        "tool_calls": [tool_call.model_dump()]  
                    })
                    
             
                    if pin:
                        function_params['pin'] = pin
                        function_response = self.names_to_functions[function_name](**function_params)
                        
                        messages.append({
                            "role": "tool",
                            "name": function_name,
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(function_response)
                        })
                response = self.client.chat.complete(
                    model=self.model,
                    messages=messages,
                )
                content = response.choices[0].message.content
            
            return {
                "content": content, 
                "success": True,
                "error": None
            }
        
        except Exception as e:
            print(e)
            return {
                "content": "Lo siento, hubo un error procesando tu mensaje.",
                "tools": [],
                "success": False,
                "error": str(e)
            }