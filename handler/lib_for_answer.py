from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message 
from aiogram.fsm.context import FSMContext

from handler.router import router
from handler.fsm import Registration
from handler.buttons import entire_keyboard, basic_keyboard
from weather_forecast.weather_web import get_weather