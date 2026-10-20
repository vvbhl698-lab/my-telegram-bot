from handler.lib_for_answer import (
    F,
    FSMContext,
    Message,
    Command,
    Registration,
    entire_keyboard,
    basic_keyboard,
    get_weather,
    router
)


@router.message(Command("start"))
@router.message(F.text.lower().replace(" ", "") == "старт")
@router.message(F.text.lower().replace(" ", "") == "сбросить")
async def hello(message: Message, state: FSMContext):
    await state.set_state(Registration.city)

    await message.delete()

    bot_message = await message.answer(
        'Привет! Это бот, который поможет тебе узнать погоду! Пожалуйста, введите название вашего города.'
        )
    
    await state.update_data(
        bot_message_id=bot_message.message_id
    )


@router.message(Registration.city)
async def get_city(message: Message, state: FSMContext):
    city = message.text.strip().lower()
    weather = await get_weather(city)

    if weather is None:
        await message.answer(
            "Город не найден",
            reply_markup=basic_keyboard
            )
    else:
        try: 
            await message.answer(
                f"""🌤 <b>Погода сегодня</b>

                <b>Состояние:</b> {weather["code"]}
                <b>Температура:</b> {weather["temperature"]} °C
                <b>Ветер:</b> {weather["wind"]} м/с
                <b>Влажность:</b> {weather["humidity"]}%
                <b>Осадки:</b> {weather["precipitation"]}
                <b>Облачность:</b> {weather["clouds"]}%""",
                reply_markup=basic_keyboard
                )
            
        except Exception as e:
            print(f"Ошибка: {e}")
            await message.answer(
                        f"Произошла неизвестная ошибка",
                        reply_markup=basic_keyboard
                        )

    await state.clear()


@router.message(Command("help"))
@router.message(F.text.lower().replace(" ", "") == "помощь")
async def help_handler(message: Message):

    await message.delete()

    await message.answer(
        '1) Старт - Запуск бота                \n' \
        '2) Помощь - Список команд             \n' \
        '3) О боте - дополнительная информация \n' \
        '4) Сбросить - Заполнить город занова',
        reply_markup=entire_keyboard
        )


@router.message(Command("about"))
@router.message(F.text.lower().replace(" ", "") == "оботе")
async def about(message: Message):

    await message.delete()

    await message.answer(
        "Скоро будет ссылка на GitHub и весь исходный код будет там (@vv2bh)"
        )


@router.message()
async def another(message: Message):

    await message.delete()

    await message.answer(
        "Команда не найдена :("
        )
