# await bot.pin_chat_message(-1001565771305, 3, False)
# await message.answer("[\.](tg://user?id=5425209307)", parse_mode=types.ParseMode.MARKDOWN_V2)
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from app.config.config import load_config 
from app.handlers.common import register_common_handlers
from app.handlers.callbacks import register_callback_handlers

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать работу"),
        BotCommand(command="/help", description="Доступные команды"),
        BotCommand(command="/cancel", description="Отменить команду")
    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        filename='log.txt',
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=load_config().tg_bot.token)
    print((await bot.get_me()).username)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    # Регистрация хэндлеров
    register_common_handlers(dp)   
    register_callback_handlers(dp)  

    # Установка команд бота     
    await set_commands(bot) 

    # Запуск поллинга                    
    await dp.start_polling()                    


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

# if __name__ == "__main__":
#     loop = asyncio.new_event_loop()
#     loop.create_task(set_commands(bot))
#     executor.start_polling(dp, skip_updates=False)