from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_keyboard(button):
    return ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)


entire_keyboard = get_keyboard([
                [KeyboardButton(text="Старт")],
                [
                    KeyboardButton(text="Помощь"), 
                    KeyboardButton(text="О боте")
                    
                ], # Две кнопки в одной строчке
                [KeyboardButton(text="Сбросить")]
                ])

basic_keyboard = get_keyboard([
                            [KeyboardButton(text="Сбросить")],
                            [KeyboardButton(text="Помощь")]
                            ])