import httpx

from weather_forecast.decoding_table import weather_codes, cities


async def get_weather(city):   
    # Получаем координаты
    async with httpx.AsyncClient() as client:
        try:
            res = cities[city]

            print("Сработал список")

        except Exception as e:
            print(f"Ошибка: {e}, переход к переводчику")
    
            try:
                translate = await client.get(
                    "https://api.mymemory.translated.net/get",
                    params={
                        "q":city,
                        "langpair": "ru|en"
                        },
                        timeout=10
                )

                translate = translate.json()
                res = translate["responseData"]["translatedText"]
        
                print("Сработал переводчик")

            except Exception as e:
                print(f"Ошибка: {e}, переводчик не сработал")
                print(f"Тип ошибки: {type(e).__name__}")
                print(f"Текст ошибки: {repr(e)}")
                return None
        

        # Проверка времени обработки запроса
        # start = time.perf_counter() # Тест
    
        try:
            params_geo = await client.get(
                "https://geocoding-api.open-meteo.com/v1/search", 
                params={"name": res, "count": 10}, timeout=10
            )

        except Exception as e:
            print(f"Ошибка: {e}, координаты не получены")
            return None


        # end = time.perf_counter() # Тест
        # print(f"Запрос на geocoding занял {end - start:.2f} секунд") # Тест

        params_geo = params_geo.json()

        if not params_geo.get("results"):
            return None

        latitude = params_geo["results"][0]["latitude"]
        longitude = params_geo["results"][0]["longitude"]

        #  Получаем данные с сайта Open-Meteo
        link_weather = "https://api.open-meteo.com/v1/forecast"

        params_weather = {"latitude": latitude,
                        "longitude": longitude,    
                        "current": [        
                            "temperature_2m",        
                            "precipitation",        
                            "wind_speed_10m",        
                            "relative_humidity_2m",       
                            "cloud_cover",        
                            "weather_code"    
                            ]
                        }

        # Проврека времени обработки запроса
        # start_1 = time.perf_counter() # Тест
        try:
            weather = await client.get(
                link_weather,
                params=params_weather, timeout=10
        )

            weather = weather.json()
        except Exception as e:
            print(f"Ошибка: {e}, данные о погоде не получены")
            return None

        
        # end_1 = time.perf_counter() # Тест
        # print(f"Запрос на Open-Meteo занял {end_1 - start_1:.2f} секунд \n") # Тест

        temperature = weather["current"]["temperature_2m"]
        wind = weather["current"]["wind_speed_10m"]
        humidity = weather["current"]["relative_humidity_2m"] # Влажность
        precipitation = weather["current"]["precipitation"] # Осадки
        clouds = weather["current"]["cloud_cover"] # Облачность
        code = weather["current"]["weather_code"] # Описание погоды

        decoding = weather_codes.get(code, "Возникла ошибка: Погода неизвестна")

        weather_info = {
            "precipitation": precipitation,
            "temperature": temperature,
            "humidity": humidity,
            "clouds": clouds,
            "wind": wind,
            "code": decoding
        }
    
        return weather_info



            
        
