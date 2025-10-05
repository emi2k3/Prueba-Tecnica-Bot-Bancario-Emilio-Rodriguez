from email import message
import logging
import os
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mistral.MistralService import MistralService
from services.CuentaService import CuentaService


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

#Inicio
ESPERANDO_PIN, MISTRAL= range(2)



mistral_service = MistralService()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['historial_mensajes'] = []
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Para poder utilizarme,porfavor ingrese el PIN de su cuenta.")
    return ESPERANDO_PIN


async def verificar_pin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    pin = update.message.text
    cuenta_service = CuentaService()
    resultado = cuenta_service.LogIn(pin)
    if not resultado:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="El PIN que ingreso es incorrecto.")
        return ESPERANDO_PIN
    context.user_data['pin'] = pin
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Bienvenido {user.first_name}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="""    
    ¿Con qué necesita ayuda?
    
    -Movimientos
    -Saldo
    -Prestamos
    -Preguntas

    """)
    return MISTRAL

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_usuario = update.message.text
    historial = context.user_data.get('historial_mensajes', [])
    pin = context.user_data.get('pin') 
    respuesta = mistral_service.procesar_mensaje(mensaje_usuario, historial, pin)
    
    if respuesta['success']:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=respuesta['content'])
        
        # Guarda en historial: user y assistant
        historial.append({"role": "user", "content": mensaje_usuario})
        historial.append({"role": "assistant", "content": respuesta['content']})
        context.user_data['historial_mensajes'] = historial
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="Hubo un problema con su consulta. Porfavor intente otra vez.")
    return MISTRAL
    

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update:{update} creo este error {context.error}")
 

if __name__ == '__main__': 
    load_dotenv() 
    token = os.getenv("token")

    application = ApplicationBuilder().token(token).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ESPERANDO_PIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, verificar_pin)],
            MISTRAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu)]
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    application.add_error_handler(error)
    application.run_polling(poll_interval=3)