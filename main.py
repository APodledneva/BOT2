from heandlers import dp
from aiogram.utils import executor


async def start_bor(_):
    print('Бот запущен')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_bor)

