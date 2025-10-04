from email import message
import logging
import os
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.CuentaService import CuentaService



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

#Inicio
ESPERANDO_PIN, MENU = range(2)
#Operaciones
PRESTAMOS_MENU,MOVIMIENTOS_MENU,PREGUNTAS =range(3)
#Movimientos
DEPOTISAR,INGRESAR,VER_ULTIMOSMOVIMIENTOS = range(3)
#Prestamos
PEDIR_PRESTAMO,PREGUNTAR_PRESTAMO,VER_PRESTAMOS_ACTUALES = range(3)




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Bienvennido {user.first_name}")
    return MENU


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"""    
    ¿Con qué necesita ayuda?
    - Movimientos
    - Prestamos
    - Preguntas
    """)



async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update:{update} creo este error {context.error}")
 

if __name__ == '__main__': 
    load_dotenv() 
    token = os.getenv("token")

    application = ApplicationBuilder().token(token).build()
    
    #Comandos
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={

            ESPERANDO_PIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, verificar_pin)],

            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu)],

           
        },
        fallbacks=[]
    )


    application.add_handler(conv_handler)

    
    #Errors
    application.add_error_handler(error)

    application.run_polling(poll_interval=3)