import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import settings
from app.db.session import engine
from app.db.middlewares import DatabaseMiddleware
from app.bot.handlers.common import router as common_router

# Configuración básica de logs para ver qué pasa en la consola
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Iniciando el bot...")

    # Instanciamos el Bot con el token y modo de parseo HTML/Markdown
    bot = Bot(
        token=settings.TELEGRAM_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # El Dispatcher maneja los eventos y FSM en memoria
    dp = Dispatcher(storage=MemoryStorage())

    # Registramos el middleware de la Base de Datos
    dp.update.outer_middleware(DatabaseMiddleware())

    # Registramos los routers de handlers
    dp.include_router(common_router)

    try:
        # Eliminamos webhooks previos si los hubiera para evitar conflictos en polling
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Bot listo y escuchando mensajes en Telegram...")
        
        # Arrancamos el bot (Polling)
        await dp.start_polling(bot)
    finally:
        # Cerramos las conexiones adecuadamente al apagar
        await bot.session.close()
        await engine.dispose()
        logger.info("Bot detenido y conexiones cerradas.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot apagado por el usuario.")
