import random
import config
from create_bot import dp
from aiogram.types import Message


@dp.message_handler(commands=['start', 'начать'])
async def mes_start(message: Message):
    await message.answer(text=f'{message.from_user.first_name}, привет! '
                              f'\nДавай поиграем в конфетную игру')


@dp.message_handler(commands=['new'])
async def mes_new_game(message: Message):
    config.total = 150
    coin = random.randint(0, 1)
    name = message.from_user.first_name

    for game in config.games:
        if message.from_user.id == game:
            await message.answer(f'{name}  ты уже есть в игре, иди играй!')
            break
    else:
        config.games[message.from_user.id] = 150
        await message.answer(text=f'Сейчас на столе {config.games[message.from_user.id]} конфет. Кидаем жеребий')
        if coin:
            await message.answer(text=f'{message.from_user.first_name},поздравляю! '
                                          f'Выпал орел. Ходи первым. Бери от 1 до 28 конфет')
        else:
            await message.answer(text=f'{message.from_user.first_name}, не расстраивайся, первый ход за ботом')
            await bot_turn(message)

@dp.message_handler()
async def all_catch(message: Message):
    if message.text.isdigit():
        if 0 < int(message.text) < 29:
            await player_turn(message)
        else:
            await message.answer(text=f'Не хитри, {message.from_user.first_name}!'
                                      f'\nКонфет нужно взять хотя бы одну, но не больше 28. Давай еще раз')
    else:
        await message.answer(text=f'Введи цифрами колличество конфет, от 1 до 28')


async def player_turn(message: Message):
    take_amount = int(message.text)
    config.games[message.from_user.id] = config.games.get(message.from_user.id) - take_amount
    name = message.from_user.first_name
    await message.answer(text=f'{name} взял {take_amount} конфет и на столе осталось '
                              f'{config.games.get(message.from_user.id)}')
    if await check_victory(message, name):
        return
    await message.answer(text=f'Передаем ход Боту!')
    await bot_turn(message)


async def bot_turn(message: Message):
    take_amount = 0
    current_total = config.games.get(message.from_user.id)
    if current_total <= 28:
        take_amount = random.randint(1, current_total)
    else:
        take_amount = random.randint(1, 28)
    config.games[message.from_user.id] = config.games.get(message.from_user.id) - take_amount
    name = message.from_user.first_name
    await message.answer(text=f'Бот взял {take_amount} конфет и на столе осталось {config.games[message.from_user.id]}')
    if await check_victory(message, 'Бот'):
        return
    await message.answer(text=f'{name} твой ход! Бери конфеты')


async def check_victory(message: Message, name: str):
    if config.games[message.from_user.id] <= 0:
        await message.answer(text=f'Победил {name}! Спасибо за игру :З')
        config.games.pop(message.from_user.id)
        return True
    return False

