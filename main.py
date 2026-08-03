import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from app.config import settings
from app.database import engine, Base
import app.database_models
from app.bot.middlewares.db_middleware import DatabaseMiddleware
from app.bot.handlers.common import router as common_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Instancia de Redis para la FSM de Aiogram
redis = Redis.from_url(settings.REDIS_URL, decode_responses=False)
storage = RedisStorage(redis=redis)

# Instancia del Bot
bot = Bot(
    token=settings.TELEGRAM_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Dispatcher con FSM guardada en REDIS
dp = Dispatcher(storage=storage)
dp.update.outer_middleware(DatabaseMiddleware())
dp.include_router(common_router)

# Ruta donde Telegram enviará los datos
WEBHOOK_PATH = f"/webhook/{settings.TELEGRAM_TOKEN}"
WEBHOOK_URL = f"{settings.WEBHOOK_URL.rstrip('/')}{WEBHOOK_PATH}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- AL ARRANCAR LA APLICACIÓN ---
    logger.info("Creando tablas en la Base de Datos si no existen...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info(f"Configurando Webhook en Telegram: {WEBHOOK_URL}")
    await bot.set_webhook(
        url=WEBHOOK_URL,
        drop_pending_updates=True
    )
    
    yield  # La aplicación se queda corriendo aquí...

    # --- AL APAGAR LA APLICACIÓN ---
    logger.info("Removiendo Webhook de Telegram...")
    await bot.delete_webhook()
    await bot.session.close()
    await engine.dispose()
    await redis.close()
    logger.info("Servidor apagado de forma limpia.")


app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    """Endpoint HTTP donde Telegram enviará las peticiones POST."""
    update_data = await request.json()
    await dp.feed_raw_update(bot, update_data)
    return Response(status_code=200)


@app.get("/")
async def health_check():
    """Ruta para verificar que el servidor está encendido."""
    return {"status": "ok", "bot": "online"}
