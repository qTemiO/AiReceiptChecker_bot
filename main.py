import asyncio
import logging
import sys

from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from settings import settings

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Отправьте чек в файле формата .pdf для анализа")


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        file_id = message.document.file_id
        file = await message.bot.get_file(file_id)
        file_path = file.file_path

        await message.bot.download_file(file_path, "validate.pdf")
    except Exception as error:
        logger.error(error)
        


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())