import asyncio
import logging
import re
import time
from datetime import datetime
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
import emoji

api = ''
logging.basicConfig(level=logging.INFO)
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

admins = [
    322972065
]


class Price(StatesGroup):
    Price = State()


class Time(StatesGroup):
    Time = State()


class Comment(StatesGroup):
    Com = State()


class Reyting(StatesGroup):
    Rey = State()


class Coords(StatesGroup):
    C1 = State()
    C2 = State()


class Order(StatesGroup):
    Or = State()


class Quantity(StatesGroup):
    Q1 = State(),
    Q2 = State(),
    Q3 = State(),
    Q4 = State(),
    Q5 = State(),
    Q6 = State(),
    Q7 = State(),
    Q8 = State(),
    Q9 = State(),
    Q10 = State(),


start_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Доставка из кафе')],
                                           # [KeyboardButton(text='Доставка из магазина')],
                                           # [KeyboardButton(text='Доставка алкоголя и табака')]
                                           ],
                                 resize_keyboard=True)

Choose_Cafe_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Момосы')],
                                                 # [KeyboardButton(text='Бургеры')],
                                                 # [KeyboardButton(text='Сэндвичи')],
                                                 # [KeyboardButton(text='Пицца')],
                                                 [KeyboardButton(text='Назад')]],
                                       resize_keyboard=True)

Food_menu_1 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Момо с курицей - 100 Rs.')],
                                            [KeyboardButton(text='Момо с овощами - 100 Rs.')],
                                            [KeyboardButton(text='Назад')]],
                                  resize_keyboard=True)

Order_menu_1 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Меню момосов')],
                                             [KeyboardButton(text='Перейти к доставке')]],
                                   resize_keyboard=True)

Order_menu_2 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Перейти к доставке')]],
                                   resize_keyboard=True)

Quantity_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='1'),
                                               KeyboardButton(text='2'),
                                               KeyboardButton(text='3'),
                                               KeyboardButton(text='4'),
                                               KeyboardButton(text='5')]],
                                    resize_keyboard=True)

Geo_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить локацию',
                                                         request_location=True)],
                                         [KeyboardButton(text='Ввести координаты')]],
                               resize_keyboard=True)

confirm_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Подтвердить заказ')],
                                             [KeyboardButton(text='Оставить комментарий')],
                                             [KeyboardButton(text='Изменить место доставки')]],
                                   resize_keyboard=True)

finish_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Доставка получена')]],
                                  resize_keyboard=True)

reyting_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(emoji.emojize(':glowing_star:')),
                                              KeyboardButton(emoji.emojize(':glowing_star::glowing_star:')),
                                              KeyboardButton(
                                                  emoji.emojize(':glowing_star::glowing_star::glowing_star:'))],
                                             [KeyboardButton(emoji.emojize(
                                                 ':glowing_star::glowing_star::glowing_star::glowing_star:')),
                                                 KeyboardButton(emoji.emojize(
                                                     ':glowing_star::glowing_star::glowing_star::glowing_star::glowing_star:'))]],
                                   resize_keyboard=True)

Citys = [
    ["деревня Керим", 400],
    ["деревня Арамболь", 300],
    ["деревня Мандрем", 300],
    ["деревня Морджим", 200],
    ["деревня Шопдем", 200],
    ["деревня Агарвадо", 200],
    ["город Сиолим", 300],
    ["Туда доставки нет"]
]

Momo = [
    ["Момо с овощами", 100],
    ["Момо с курицей", 100],
    ["Момо с сыром и шпинатом", 200],
]

Basket_List = []
Locate_list = []
Total_price = []
Prices = []


start = (f"Бот создан для доставки по Северному Гоа, "
         f"\nВремя работы с 12 дня до 12 ночи"
         f"\nот Сиолима до Керима. "
         f"\nВ данный момент следующие расценки на доставку:"
         f"\nСиолим - 300 Rs "
         f"\nМорджим - 200 Rs "
         f"\nМандрем - 300 Rs "
         f"\nАрамболь - 300 Rs "
         f"\nКерим - 400 Rs "
         f"\nЧтобы сейчас получить доставку из аптеки или магазина, "
         f"\nнапишите команду /order "
         f"\nАдминистратор может связаться для уточнения информации."
         f"\nДоставка личных посылок возможна, но только после проверки их на легальность."
         f"\nДля заказа нажмите /start")


times = datetime(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour,
                 datetime.now().minute)

@dp.message_handler(commands=['help'])
async def bot_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! "
        f"\n{start}",
        reply_markup=start_menu)


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message, state: FSMContext):
    t = str(message.date.time())
    print(message.from_user, t)
    # await state.update_data(Time=)
    if times.hour == 0 or times.hour == 1 or times.hour == 2 or times.hour == 3 or times.hour == 4 \
            or times.hour == 5 or times.hour == 6 or times.hour == 7 or times.hour == 8 or times.hour == 9 or times.hour == 10 \
            or times.hour == 11:
        await bot.send_message(message.from_user.id, f'Прием заказов с 12:00 до 00:00',
                               reply_markup=types.ReplyKeyboardRemove())
        while times.hour < 12:
            time.sleep(120)
    else:
        await message.answer(f"Привет, {message.from_user.full_name}! "
                             f"\n{start}",
                             reply_markup=start_menu)
    data = await state.get_data()
    Rey = data.get("Rey")
    ti = 0
    while ti < 75 or Rey == "":
        await asyncio.sleep(60)
        ti += 1
    else:
        await message.answer(f"Сессия сброшена. Начните свой заказ заново",
                             reply_markup=start_menu)
    Basket_List.clear()
    Locate_list.clear()
    Prices.clear()



@dp.message_handler(commands=['order'])
async def bot_start(message: types.Message, state: FSMContext):
    if times.hour == 12 or times.hour == 0 or times.hour == 1 or times.hour == 2 or times.hour == 3 or times.hour == 4 \
            or times.hour == 5 or times.hour == 6 or times.hour == 7 or times.hour == 8 or times.hour == 9 or times.hour == 10 \
            or times.hour == 11:
        await bot.send_message(message.from_user.id, f'Прием заказов с 12:00 до 00:00',
                               reply_markup=types.ReplyKeyboardRemove())
        time.sleep(120)
    else:
        await message.answer('Напишите содержание заказа. Только то, что можно достать в наших магазинах и аптеках',
                             reply_markup=types.ReplyKeyboardRemove())
        await Order.Or.set()


@dp.message_handler(state=Order.Or)
async def bot_start(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    order = message.text
    await state.update_data(order=order)
    Basket_List.append(order)
    await bot.send_message(chat_id=chat_id,
                           text='Выберете место доставки',
                           reply_markup=Geo_menu)
    await state.reset_state(with_data=True)


# --------------------------------------------
# --------------------------------------------
# --------------------------------------------
# --------------------------------------------


@dp.message_handler(Text(equals=['Доставка из кафе']))
async def starter(message: types.Message):
    if times.hour == 0 or times.hour == 1 or times.hour == 2 or times.hour == 3 or times.hour == 4 \
            or times.hour == 5 or times.hour == 6 or times.hour == 7 or times.hour == 8 or times.hour == 9 or times.hour == 10 \
            or times.hour == 11:
        await bot.send_message(message.from_user.id, f'Прием заказов с 12:00 до 00:00',
                               reply_markup=types.ReplyKeyboardRemove())
        while times.hour < 12:
            time.sleep(120)
    else:
        await message.answer('Выберете категорию', reply_markup=Choose_Cafe_menu)


@dp.message_handler(Text(equals=['Назад']))
async def starter(message: types.Message):
    await message.answer('Назад', reply_markup=start_menu)


@dp.message_handler(Text(equals=['Момосы']))
async def starter(message: types.Message):
    chat_id = message.chat.id
    await bot.send_photo(chat_id=chat_id, caption="Выберете момо. Доставка из ChillOut Cafe",
                         photo='https://www.drukgirl.com/wp-content/uploads/2020/05/cabbage-momos-recipe.jpg',
                         reply_markup=Food_menu_1)
    await Quantity.Q1.set()


@dp.message_handler(Text(equals=['Назад']))
async def starter(message: types.Message):
    await message.answer('Назад', reply_markup=Choose_Cafe_menu)


@dp.message_handler(Text(equals=['Момо с овощами - 100 Rs.']))
async def starter(message: types.Message, state: FSMContext):
    answer1 = "Момо с овощами"
    await state.update_data(answer1=answer1)
    await message.answer('Сколько порций кладем в заказ?', reply_markup=Quantity_menu)
    Prices.append(Momo[1[2]])
    await Quantity.Q2.set()


@dp.message_handler(Text(equals=['Момо с курицей - 100 Rs.']))
async def starter(message: types.Message, state: FSMContext):
    answer1 = "Момо с курицей"
    await state.update_data(answer1=answer1)
    await message.answer('Сколько порций кладем в заказ?', reply_markup=Quantity_menu)
    Prices.append(Momo[2[2]])
    await Quantity.Q2.set()


@dp.message_handler(Text(equals=['Назад']))
async def starter(message: types.Message):
    await message.answer('Назад', reply_markup=Food_menu_1)


@dp.message_handler(Text(equals=["1", "2", "3", "4", "5"]))
async def starter(message: types.message, state: FSMContext):
    answer2 = message.text
    data = await state.get_data()
    answer1 = data.get("answer1")
    await state.update_data(answer2=answer2)
    Basket_List.append(answer1)
    Basket_List.append(answer2)
    await state.reset_state(with_data=True)
    if len(Basket_List) == 4:
        a1 = Basket_List[0]
        a2 = Basket_List[1]
        a3 = Basket_List[2]
        a4 = Basket_List[3]
        await message.answer(f"Вы выбрали {a1},{a2} шт. И {a3}, {a4} шт. "
                             f"Что-нибудь ещё?",
                             reply_markup=Order_menu_2)
    else:
        a1 = f"{answer1}, {answer2} шт."
        await message.answer(f"Вы выбрали {a1} "
                             f"Что-нибудь ещё?",
                             reply_markup=Order_menu_1)


@dp.message_handler(Text(equals=['Перейти к доставке']))
async def starter(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if len(Basket_List) == 4:
        a = Basket_List[1]
        b = Basket_List[3]
        if Basket_List[2] == Momo[1[1]]:
            p = int(a) * Prices[1] + int(b) * Prices[2]
        elif Basket_List[2] == Momo[2[1]]:
            p = int(a) * Prices[2] + int(b) * Prices[1]
        await state.update_data(p=p)
        await bot.send_message(chat_id=chat_id,
                               text=f"Заказ на {p} Rs. "
                                    f"Выберете локацию",
                               reply_markup=Geo_menu)
    else:
        a = Basket_List[1]
        if Basket_List[2] == Momo[1[1]]:
            p = int(a) * Prices[1]
        elif Basket_List[2] == Momo[2[1]]:
            p = int(a) * Prices[2]
        await state.update_data(p=p)
        await bot.send_message(chat_id=chat_id,
                               text=f"Заказ на {p} Rs. "
                                    f"Выберете локацию",
                               reply_markup=Geo_menu)
    


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def get_location(message: types.Message, state: FSMContext):
    location = message.location
    lat = location.latitude
    lon = location.longitude
    Locate_list.append(lat)
    Locate_list.append(lon)
    token = 'dbbc745a-3a34-421b-850b-6467f68ba8da'
    url = f'https://geocode-maps.yandex.ru/1.x/?apikey={token}&geocode={lon},{lat}&format=json'
    try:
        result = requests.get(url)
        data = result.json()
        address_str = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
            "GeocoderMetaData"]["AddressDetails"]["Country"]["AdministrativeArea"]["SubAdministrativeArea"]["Locality"][
            "LocalityName"]
    except Exception as e:
        chat_id = message.chat.id
        return await bot.send_message(chat_id=chat_id, text="error")
    for i in Citys:
        if address_str == Citys[0][0]:
            d = Citys[0]
            break
        elif address_str == Citys[1][0]:
            d = Citys[1]
            break
        elif address_str == Citys[2][0]:
            d = Citys[2]
            break
        elif address_str == Citys[3][0]:
            d = Citys[3]
            break
        elif address_str == Citys[4][0]:
            d = Citys[4]
            break
        elif address_str == Citys[5][0]:
            d = Citys[5]
            break
        elif address_str == Citys[6][0]:
            d = Citys[6]
            break
        else:
            d = Citys[7]
            break
    if d == Citys[7]:
        chat_id = message.chat.id
        await bot.send_message(chat_id=chat_id, text=f"{d[0]}. "
                                                     f"Выберете другой адрес",
                               reply_markup=Geo_menu)
    else:
        data = await state.get_data()
        p = data.get("p")
        c = d[1] + p
        Price = c
        await state.update_data(Price=Price)
        Total_price.append(Price)
        chat_id = message.chat.id
        await bot.send_message(chat_id=chat_id, text=f"Ваше место {address_str}. Стоимость доставки {d[1]} Rs. "
                                                     f"Всего к оплате {c} Rs.",
                               reply_markup=confirm_menu)


@dp.message_handler(Text(equals=['Ввести координаты']))
async def bot_start(message: types.Message):
    await message.answer(f"Введите координаты", reply_markup=types.ReplyKeyboardRemove())
    await Coords.C1.set()


@dp.message_handler(state=Coords.C1)
async def starter(message: types.message, state: FSMContext):
    Lok = message.text
    await state.update_data(Lok=Lok)
    data = await state.get_data()
    Lok = data.get("Lok")
    lst = Lok.split()
    lat = lst[0]
    lon = lst[1]
    Locate_list.append(lat)
    Locate_list.append(lon)
    token = 'dbbc745a-3a34-421b-850b-6467f68ba8da'
    url = f'https://geocode-maps.yandex.ru/1.x/?apikey={token}&geocode={lon},{lat}&format=json'
    print(url)
    try:
        result = requests.get(url)
        data = result.json()
        address_str = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
            "GeocoderMetaData"]["AddressDetails"]["Country"]["AdministrativeArea"]["SubAdministrativeArea"]["Locality"][
            "LocalityName"]
    except Exception as e:
        chat_id = message.chat.id
        return await bot.send_message(chat_id=chat_id, text="error")
    for i in Citys:
        if address_str == Citys[0][0]:
            d = Citys[0]
            break
        elif address_str == Citys[1][0]:
            d = Citys[1]
            break
        elif address_str == Citys[2][0]:
            d = Citys[2]
            break
        elif address_str == Citys[3][0]:
            d = Citys[3]
            break
        elif address_str == Citys[4][0]:
            d = Citys[4]
            break
        elif address_str == Citys[5][0]:
            d = Citys[5]
            break
        elif address_str == Citys[6][0]:
            d = Citys[6]
            break
        else:
            d = Citys[7]
            break
    data = await state.get_data()
    p = data.get("p")
    if d == Citys[7]:
        chat_id = message.chat.id
        await bot.send_message(chat_id=chat_id, text=f"{d[0]}. "
                                                     f"Выберете другой адрес",
                               reply_markup=Geo_menu)
    elif p == None:
        chat_id = message.chat.id
        await bot.send_message(chat_id=chat_id, text=f"Ваше место {address_str}. Стоимость доставки {d[1]} Rs. "
                                                     f"Оплата товаров рассчитывается по чеку.",
                               reply_markup=confirm_menu)
    else:
        # data = await state.get_data()
        # p = data.get("p")
        c = d[1] + p
        Price = c
        await state.update_data(Price=Price)
        Total_price.append(Price)
        chat_id = message.chat.id
        await bot.send_message(chat_id=chat_id, text=f"Ваше место {address_str}. Стоимость доставки {d[1]} Rs. "
                                                     f"Всего к оплате {c} Rs.",
                               reply_markup=confirm_menu)
    await state.reset_state(with_data=True)


@dp.message_handler(Text(equals=['Изменить место доставки']))
async def starter(message: types.Message):
    await message.answer('Изменить место доставки', reply_markup=Geo_menu)


@dp.message_handler(Text(equals=['Оставить комментарий']))
async def starter(message: types.Message, state: FSMContext):
    await message.answer('Если Вам есть что добавить, оставьте комментарий', reply_markup=types.ReplyKeyboardRemove())
    await Comment.Com.set()


@dp.message_handler(state=Comment.Com)
async def starter(message: types.Message, state: FSMContext):
    Com = message.text
    chat_id = message.chat.id
    await state.update_data(Com=Com)
    l1 = Locate_list[0]
    l2 = Locate_list[1]
    admin_id = admins[0]
    u = message.from_user
    if len(Total_price) == 0:
        await bot.send_message(chat_id=admin_id, text=f"{u}"
                                                      f"{Basket_List},")
        await bot.send_message(chat_id=admin_id, text=f"{l1} {l2}")
    else:
        P1 = Total_price[0]
        await bot.send_message(chat_id=admin_id, text=f"{u}"
                                                      f"{Basket_List}, {P1} Rs")
        await bot.send_message(chat_id=admin_id, text=f"{l1} {l2}")
    await bot.send_message(chat_id=chat_id, text='Спасибо за заказ. Курьер приедет в течении часа.',
                           reply_markup=finish_menu)
    await state.reset_state(with_data=True)


@dp.message_handler(Text(equals=['Подтвердить заказ']))
async def starter(message: types.Message):
    await message.answer('Спасибо за заказ. Курьер приедет в течении часа.',
                         reply_markup=finish_menu)
    l1 = Locate_list[0]
    l2 = Locate_list[1]
    admin_id = admins[0]
    u = message.from_user
    t = message.date
    if len(Total_price) == 0:
        await bot.send_message(chat_id=admin_id, text=f"{u}"
                                                      f"\n{t}"
                                                      f"{Basket_List},")
        await bot.send_message(chat_id=admin_id, text=f"{l1} {l2}")
    else:
        P1 = Total_price[0]
        await bot.send_message(chat_id=admin_id, text=f"{u}"
                                                      f"\n{t}"
                                                      f"{Basket_List}, {P1} Rs")
        await bot.send_message(chat_id=admin_id, text=f"{l1} {l2}")



@dp.message_handler(Text(equals=['Доставка получена']))
async def starter(message: types.Message):
    await message.answer(f"Приятного аппетита, обращайтесь снова! "
                         f"Оцените нашу работу",
                         reply_markup=reyting_menu)
    await Reyting.Rey.set()


@dp.message_handler(state=Reyting.Rey)
async def starter(message: types.Message, state: FSMContext):
    Rey = message.text
    t = message.date
    await state.update_data(Com=Rey)
    admin_id = admins[0]
    await bot.send_message(chat_id=admin_id, text=f"{Rey}"
                                                  f"\n{t}")
    await message.answer('Благодарим за оценку',
                         reply_markup=start_menu)
    await state.reset_state(with_data=True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
