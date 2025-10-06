import os
from mistralai import Mistral
from dotenv import load_dotenv
import json
import logging
from services.PrestamoService import PrestamoService
from services.CuentaService import CuentaService
from services.MovimientoService import MovimientoService  

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
load_dotenv()
cuenta_service = CuentaService()  
movimiento_service = MovimientoService()  
prestamo_service = PrestamoService()

class MistralService:
    """ IA que toma el contexto del chat de telegram y responde al usuario según prompt y tools."""
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.model = "mistral-large-latest"
        self.client = Mistral(api_key=self.api_key)
        #Cuenta
        def consultar_saldo(pin):
            return cuenta_service.consultarSaldo(pin)  
        def plazofijo(pin,dias,monto):
            return cuenta_service.plazofijo(pin,dias,monto)  
        #Movimientos
        def verUltimosMovimientos(pin):
            return movimiento_service.verUltimosMovimientos(pin)  
        #Prestamos
        def consultarPrestamos(pin):
            return prestamo_service.consultarPrestamos(pin)  
        def consultarCuotasdeUnPrestamo(fecha_prestamo, pin):
            prestamos = prestamo_service.consultarPrestamos(pin)
    # Buscar el préstamo que coincide con la fecha
            prestamo = next((p for p in prestamos if p["fecha_otorgamiento"] == fecha_prestamo), None)
            if not prestamo:
                return {"mensaje": "No se encontró un préstamo con esa fecha o ya está pagado."}
            return prestamo_service.consultarCuotasdeUnPrestamo(prestamo["id_prestamo"],pin)   

        def interesTotal(monto:int,cuotas:int,pin):
            return prestamo_service.interesTotal(monto,cuotas,pin)  
        def pedirPrestamo(monto:int,cuotas:int,pin):
            return prestamo_service.pedirPrestamo(pin,monto,cuotas) 
        def isMoroso(pin):
            return prestamo_service.isMoroso(pin)  


        #Para que mistral pueda llamar a las funciones
        self.names_to_functions = {
            'consultarSaldo': consultar_saldo,
            'verUltimosMovimientos': verUltimosMovimientos,
            'consultarPrestamos': consultarPrestamos,
            'consultarCuotasdeUnPrestamo': consultarCuotasdeUnPrestamo,
            'interesTotal': interesTotal,
            'pedirPrestamo': pedirPrestamo,
            'isMoroso': isMoroso,
            'plazofijo':plazofijo
        }
        # Para que mistral entienda que funciones tiene disponible y para que utilizarlas
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
            "description": "Obtiene todos los préstamos pendientes del usuario. ESTA TOOL DEBE SER LLAMADA cada vez que el usuario mencione préstamos. El modelo no debe inventar información sobre préstamos ni fechas. Si la tool devuelve [] (vacío), responde: 'No tienes préstamos pendientes en este momento.' No muestres ids internos. Termina preguntando: '¿Quieres ver las cuotas de algún préstamo específico? Indícame la fecha.",
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
            "description": "Obtiene las cuotas pendientes de un préstamo específico. Llama esta tool solo después de haber llamado 'consultarPrestamos' o si el usuario proporciona la fecha del préstamo. Requiere la fecha en formato YYYY-MM-DD (conviértela si el usuario la da naturalmente). Si no hay cuotas pendientes, responde: 'Este préstamo ya está pagado.' Si hay, solo lista las cuotas de forma clara y termina preguntando '¿Qué más necesitas?'",
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
    },
      {
        "type": "function",
        "function": {
            "name": "interesTotal",
            "description": "Obtiene el total a pagar según la cuota y el monto que pide el usuario, si el usuario es moroso los intereses pueden ser mayores. Llama esta tool si el usuario proporciona una cuota y un monto para consultar cuanto le saldría pedir un prestamo. Solo lista los resultados de forma clara y termina preguntando '¿Qué más necesitas?'",
            "parameters": {
                "type": "object",
                "properties": {
                    "cuotas": {
                        "type": "number",
                        "description": "La cuota son los meses en lo cuales se piensa pagar el prestamo. El mínimo es 2 y el máximo es 36 Por ejemplo: Quiero pedir un prestamo de 20000 pesos en 12 cuotas, si el usuario no lo proporciona, insistirle. NO PERMITIR VALORES FUERA DE RANGO"
                    },
                    "monto": {
                        "type": "number",
                        "description": "El monto que el usuario esta pidiendo, si no da un monto insistir a que de uno. El mínimo es 10000. NO PERMITIR VALORES FUERA DE RANGO"
                    }
                },
                "required": ["cuotas","monto"]
            }
        }
    },
     {
        "type": "function",
        "function": {
            "name": "pedirPrestamo",
            "description": "Procesa una solicitud de préstamo. Retorna true si se aprobó el préstamo, false si se rechazó (solo si el usuario tiene 2 o más préstamos activos). Los usuarios morosos SI pueden obtener préstamos pero con tasas de interés más altas. Llama esta tool cuando el usuario solicite un préstamo con monto y cuotas. Informa el resultado y pregunta '¿Qué más necesitas?'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cuotas": {
                        "type": "number",
                        "description": "La cuota son los meses en lo cuales se piensa pagar el prestamo. El mínimo es 2 y el máximo es 36 Por ejemplo: Quiero pedir un prestamo de 20000 pesos en 12 cuotas, si el usuario no lo proporciona, insistirle. NO PERMITIR VALORES FUERA DE RANGO"
                    },
                    "monto": {
                        "type": "number",
                        "description": "El monto que el usuario esta pidiendo, si no da un monto insistir a que de uno. El mínimo es 10000 y el máximo es 500000. NO PERMITIR VALORES FUERA DE RANGO"
                    }
                },
                "required": ["cuotas","monto"]
            }
        }
    },
         {
        "type": "function",
        "function": {
            "name": "isMoroso",
            "description": "Obtiene true si el cliente es moroso, false si no, si el cliente es moroso, la tasa de interes va a ser más alta. NO LE DIGAS AL USUARIO QUE PUEDES HACER ESTO",
            "parameters": {
                "type": "object",
                "properties": {
                    
                },
                "required": []
            }
        }
    },
     {
        "type": "function",
        "function": {
            "name": "plazofijo",
            "description": "Calcula si al cliente le conviene hacer un plazo fijo con el monto y los días ingresados. Llama esta tool cuando el usuario diga 'quiero hacer un plazo fijo', 'plazo fijo de X días' o algo similar. Si el usuario da un plazo fuera del rango 181–1096 días, respóndele que los únicos plazos disponibles son entre 181–1096 días, sin llamar la tool. Si el resultado es positivo, explica brevemente el rendimiento y pregunta '¿Qué más necesitas?'. Si no conviene, indícalo también y pregunta lo mismo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dias": {
                        "type": "number",
                        "description": "La cantidad de días en la cual el usuario va a hacer el plazo fijo, el mínimo es de 181 días y el máximo es de 1096. "
                    },
                    "monto": {
                        "type": "number",
                        "description": "El monto que el usuario va a ingresar para el plazo fijo, si no da un monto insistir a que de uno. El monto mínimo es de 5000. NO PERMITIR VALORES FUERA DE RANGO"
                    }
                },
                "required": ["dias","monto"]
            }
        }
    }
  
]
    
    def procesar_mensaje(self, mensaje_usuario, historial_mensajes=None, pin=None):
        """Función encargada de tomar los mensajes y el historial del usuario, el pin esta para que la IA no lo pida otra vez. """
        messages = []
        #Promp inicial para el bot, le da contexto y le dice que hacer.
        messages.append({
            "role": "system",
            "content": """
            Eres un bot bancario de Telegram para el Bank of Uruguay, un banco uruguayo. Responde de manera amigable, concisa y útil. Siempre usa las tools disponibles para consultar datos reales, NO inventes información, ni ofrezcas funcionalidades que NO tienes. 

Instrucciones clave:
- No saludes ni digas 'Hola', ya que el usuario ya inició sesión.
- El usuario ya tiene una cuenta con el banco, ya que inició sesión en el sistema.
- Todas las respuestas deben estar en español, incluyendo las generadas tras usar tools. No uses inglés bajo ninguna circunstancia.
- Distingue claramente: Si el usuario menciona 'préstamos', 'préstamos pendientes' o similar sin especificar 'pedir' o 'solicitar', asume que quiere consultar sus préstamos actuales y llama automáticamente 'consultarPrestamos'. Solo si dice explícitamente 'quiero pedir un préstamo' o similar, procede con 'interesTotal' o 'pedirPrestamo'.
- Si menciona 'movimientos' sin especificar, pregunta: '¿Quieres ver tus últimos movimientos? Confírmame para consultar.' Y no agregues nada más en esa respuesta.
- Para consultas de préstamos, llama automáticamente la función consultarPrestamos para mostrar sus préstamos actuales. Termina con: '¿Quieres ver las cuotas de algún préstamo específico? Indícame la fecha.'
Si el usuario menciona "préstamo", "préstamos", "préstamos pendientes", "tengo préstamos" o cualquier variación, **NO** respondas nada sobre préstamos sin antes llamar a la tool consultarPrestamos. Siempre llama consultarPrestamos y usa únicamente los datos que esa tool devuelva. No inventes préstamos ni fechas. Si la tool devuelve lista vacía, responde exactamente: "No tienes préstamos pendientes en este momento."
- Para pedir un préstamo nuevo, confirma primero monto y cuotas, menciona siempre los rangos completos: mínimo monto 10000 pesos, máximo 500000 pesos; mínimo cuotas 2, máximo 36. Si los valores están fuera, insiste sin procesar.
- Después de entregar datos de una tool (excepto consultarPrestamos), resume brevemente si es necesario y siempre termina preguntando: '¿Qué más necesitas?'
- Si no hay datos (e.g., no hay préstamos), informa amigablemente: 'No tienes préstamos pendientes en este momento.' Sin llamar tools innecesarias.
- Maneja fechas naturalmente: convierte formatos como '2 de septiembre de 2023' a 'YYYY-MM-DD' antes de pasar a tools.
- No muestres IDs internos como 'id_prestamo'. Formatea respuestas limpias, sin asteriscos ni markup extra.
- Si el usuario pregunta algo no cubierto por las tools, di: 'Lo siento, solo puedo ayudarte con saldo, movimientos y préstamos por ahora.'
- Mantén respuestas cortas: resume si la lista es larga (e.g., muestra solo las próximas 5 cuotas y ofrece ver más si el usuario pide).
- Si pregunta por que tarjetas ofrecemos, o que tarjeta ofrecen diles que: "Ofrecemos tarjetas de crédito y débito, Visa y Mastercard." Y nada más, no existen otras tarjetas en nuestro banco.
- Si el usuario pone preguntas comunes o preguntas dile que le puedes informar sobre:
 Tarjetas que ofrecemos en nuestro banco.
 Tasa para préstamos personales.
 Si le conviene hacer plazos fijos.
 NO agregues nada más.
-La tasa para préstamos personales es de:
De 2 a 6 cuotas la tasa anual es del 27%
De 7 a 12 cuotas la tasa anual es del 30%
De 13 a 24 cuotas la tasa anual es del 31%
De 25 a 36 cuotas la tasa anual es del 32%
Si el usuario pide un plazo fijo con una cantidad de días fuera del rango permitido (181 a 1096), respóndele: 'Actualmente solo ofrecemos plazos fijos entre 181 y 1096  días.' y no llames ninguna tool. El monto mínimo es de 5000. NO PERMITIR VALORES FUERA DE RANGO
IMPORTANTE: Los usuarios morosos (con cuotas vencidas) pueden obtener préstamos pero con tasas de interés más altas (+15% adicional). Siempre informa esto al usuario moroso antes de procesar su solicitud. Ten en cuenta que la tasa máxima de interés es 45%.
Instrucciones adicionales para formateo:
- Siempre usa texto plano en las respuestas. NO uses Markdown como **negrita**, *cursiva*, ni listas con asteriscos (*) a menos que sea para tablas (usa | para columnas).
    """
        })
        
        if historial_mensajes:
            #Si ya existe un historial de mensajes, que siga desde ahí.
            messages.extend(historial_mensajes)
              
        #Agrega el nuevo mensaje del usuario al array de mensajes
        messages.append({
            "role": "user",
            "content": mensaje_usuario
        })

        try:
            #Llama a Mistral, le pasa el modelo,los mensajes, las herramientas y la manera de elegir las herramientas.
            #Esto retorna un array de elecciones.
            response = self.client.chat.complete(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
                parallel_tool_calls=False,
            )
          
            assistant_message = response.choices[0].message
            
            #Por si no retorna nada, que no de error
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
                    
                    #Le pasa pin a todas las funciones
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
                
                #Saca el mensaje de la primera elección 
                content = response.choices[0].message.content
            
            return {
                "content": content, 
                "success": True,
                "error": None
            }
        
        #En caso de error lo muestra en consola y el bot retorna un mensaje al usuario informandole sobre el problema.
        except Exception as e:
            logging.info(e)
            return {
                "content": "Lo siento, hubo un error procesando tu mensaje.",
                "tools": [],
                "success": False,
                "error": str(e)
            }
