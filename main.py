from os import getenv
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from handler.answer import router


load_dotenv()
TOKEN = getenv("BOT_TOKEN")

bot = Bot(
    token=TOKEN, 
    default=DefaultBotProperties(parse_mode="HTML"))

dp = Dispatcher()

dp.include_router(router)


async def main():
    print("Start...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())