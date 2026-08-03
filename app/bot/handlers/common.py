from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import UserService
from app.services.ai_service import AIService

router = Router()

#Definimos los estados para el usuario
class ChatState(StatesGroup):
    chatting = State()  # El usuario está conversando con la IA

#Creamos el menú principal con botones
def get_main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Hablar con la IA")],
        ],
        resize_keyboard=True
    )
    return keyboard

#Comando /start
@router.message(CommandStart())
async def cmd_start(message: Message, db: AsyncSession, state: FSMContext):
    """Maneja /start, registra al usuario y muestra el menú."""
    await state.clear()  # Limpiamos cualquier estado previo
    
    tg_user = message.from_user
    if not tg_user:
        return

    user = await UserService.get_or_create_user(
        db=db,
        telegram_id=tg_user.id,
        username=tg_user.username,
        first_name=tg_user.first_name,
        last_name=tg_user.last_name
    )

    await message.answer(
        f"¡Hola, {user.first_name}! \n\nBienvenido. Selecciona una opción del menú:",
        reply_markup=get_main_menu()
    )

#Opción para ENTRAR al modo IA
@router.message(F.text == "Hablar con la IA")
async def enter_ai_mode(message: Message, state: FSMContext):
    # Cambiamos el estado del usuario a 'chatting'
    await state.set_state(ChatState.chatting)
    
    # Teclado para salir del chat
    exit_keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Salir del chat")]],
        resize_keyboard=True
    )
    
    await message.answer(
        "**Modo IA Activado**\n\n"
        "Escríbeme lo que quieras. Para regresar al menú principal, presiona el botón 'Salir del chat' o usa /menu.",
        reply_markup=exit_keyboard
    )

#Opción para SALIR del modo IA o volver al menú
@router.message(F.text == "Salir del chat")
@router.message(Command("menu"))
async def exit_ai_mode(message: Message, state: FSMContext):
    await state.clear()  # Salimos del estado
    await message.answer(
        "Has vuelto al menú principal.",
        reply_markup=get_main_menu()
    )

#Responder con la IA SOLO SI el usuario está en el estado 'chatting'
@router.message(ChatState.chatting, F.text)
async def handle_ai_chat(message: Message):
    if not message.text:
        return

    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    ai_response = await AIService.generate_response(prompt=message.text)
    await message.answer(ai_response)
