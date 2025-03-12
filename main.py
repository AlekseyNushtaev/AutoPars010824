import asyncio
import logging
import time

from aiogram.exceptions import TelegramNetworkError

import handlers

from aiogram import Dispatcher

from bot import bot


logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format='%(filename)s:%(lineno)d %(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')
    logging.info('Starting bot')
    loop = asyncio.get_event_loop()
    await loop.create_task(handlers.scheduler())

    dp = Dispatcher()
    dp.include_router(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    while True:
        try:
            await dp.start_polling(bot, polling_timeout=100, close_bot_session=False)
        except TelegramNetworkError as err:
            print(err)
            print('* Connection failed, waiting to reconnect...')
            time.sleep(1)
            print('* Reconnecting.')

if __name__ == '__main__':
    asyncio.run(main())
