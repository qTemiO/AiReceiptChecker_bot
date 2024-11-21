from pathlib import Path
import asyncio
import logging
import sys

import torch
from loguru import logger
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReactionTypeEmoji

from utils import get_save_path, is_already_in_fakes
from settings import settings
from templates import (
    form_pdf_metadata_reply,
    form_pdf_signature_reply
)
from operations import (
    z_check, 
    producer_check, 
    meta_check,
    signature_check
)

dp = Dispatcher()
device = "cuda" if torch.cuda.is_available() else "cpu"

models_path = Path(__file__).parent.joinpath("models")

model = AutoModelForSequenceClassification.from_pretrained(models_path.joinpath("best").__str__(), num_labels=2)
model.to(device)
tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-cased")
logger.success("Models loaded")

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer("Отправьте чек в файле формата .pdf для анализа")


@dp.callback_query(F.data == "mark_as_fake")
async def mark_as_fake(callback: CallbackQuery):
    try:
        reaction_type = "👎" if is_already_in_fakes(callback.message.reply_to_message.document.file_name) else "👍"
        await callback.message.react(reaction=[ReactionTypeEmoji(emoji=reaction_type)])
    except Exception as e:
        await callback.message.reply(text="Файл не найден на сервере")
        
@dp.message()
async def pdf_handler(message: Message) -> None:
    try:        
        # Получаем файл с серверов телеги
        file_id = message.document.file_id
        file = await message.bot.get_file(file_id)
        file_path = file.file_path
        file_pdf_path = get_save_path(message.document.file_name)
        await message.bot.download_file(file_path, file_pdf_path)

        # Проверка метаданных
        z_check_result = z_check(file_pdf_path)
        producer_check_result = producer_check(file_pdf_path)
        meta_check_result = meta_check(file_pdf_path)
        metadata_text = form_pdf_metadata_reply(
            z_check_result, 
            producer_check_result, 
            meta_check_result
        )

        # Сигнатурная проверка
        signature_check_result = signature_check(
            file_pdf_path, 
            tokenizer, 
            model
        )
        signature_text = form_pdf_signature_reply(signature_check_result)

        # Ответ пользователю
        total_block = f"{metadata_text} \n\n {signature_text}"

        # Создаём кнопки
        fake = InlineKeyboardButton(text="Отметить как фейк", callback_data="mark_as_fake")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[fake]])

        await message.reply(total_block, reply_markup=keyboard)
        
    except Exception as error:
        logger.error(error)
        await message.bot.send_message(message.chat.id, "Пожалуйста, отправьте корректный .pdf файл")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())