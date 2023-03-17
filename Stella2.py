import random
import wmi
import os
import threading
import winsound
import json
import re
import datetime
from bs4 import BeautifulSoup
import pyttsx3
import pyaudio
import wave
import geocoder
import wikipedia
import requests
import webbrowser
import time
import pyautogui
import keyboard
import speech_recognition as sr
import langdetect

current_time = datetime.datetime.now().time()

def search_in_browser():

    webbrowser.open("https://www.chrome.com")
    speak("Открываю Гугл Хром")

    time.sleep(2)
    keyboard.press_and_release('ctrl+l')

    search_term = re.search('найди (.+)', query)
    if search_term:
        search_term = search_term.group(1).replace(' ', '_')
        keyboard.write(search_term)
        # запрашиваем новый запрос и вводим его в адресную строку
        keyboard.press_and_release('enter')





r = sr.Recognizer()


# Замените <API_KEY> на ваш собственный API ключ от OpenWeatherMap
api_key = '78de1db61ffa6efd32239911ca57f068'
weather_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={api_key}&lang=ru"

# Язык ассистента
language = 'ru'

# Имя ассистента
name = 'Stella'






# Функция для распознавания речи
def recognize_speech(index=0):
    r = sr.Recognizer()
    with sr.Microphone(device_index=index) as source:
        print("Говорите...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, phrase_time_limit=5)
        r.energy_threshold = 5000  # установка порога в 4000 дБ

    try:

        voice_input = r.recognize_google(audio, language="ru-RU").lower()
        print(f">>> {voice_input}")
        return voice_input
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Извините, не могу соединиться с сервером распознавания речи. Возможно у вас отключен интернет")
        return ""


def play_pause():
    keyboard.press_and_release('k')


def next_video():
    keyboard.press_and_release('l')


def previous_video():
    keyboard.press_and_release('j')



#озвучивание речи
def speak(text, lang='ru', voice_idx=0):
    engine = pyttsx3.init()
    engine.setProperty('rate', 210)  # скорость воспроизведения текста
    engine.setProperty('volume', 1)  # громкость
    voices = engine.getProperty('voices')
    if lang == 'ru':
        engine.setProperty('voice', voices[voice_idx].id)
    elif lang == 'en':
        engine.setProperty('voice', voices[voice_idx + 1].id)  # второй голос для английского языка
    else:
        print('Unsupported language!')
        return

    # конвертируем текст в аудиофайл
    engine.save_to_file(text, 'response.wav')
    engine.runAndWait()

    # проигрываем аудиофайл с помощью pyaudio
    wf = wave.open('response.wav', 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    # закрываем все соединения
    stream.stop_stream()
    stream.close()
    p.terminate()








def play_video():
    # Открываем браузер
    webbrowser.open("https://www.youtube.com")

    # Ожидаем загрузки страницы
    time.sleep(5)

    # Нажимаем на поле поиска
    pyautogui.click(600, 200)

    search_term = re.search(' видео (.+)', query)
    if search_term:
        search_term = search_term.group(1).replace(' ', '_')
    # Проверяем, что запрос не пустой

        # Вводим запрос в строку поиска
        keyboard.write(search_term)
        time.sleep(1)
        keyboard.press("enter")

        # Ожидаем загрузки страницы
        time.sleep(2)

        # Нажимаем на первое видео
        pyautogui.click(350, 400)

        # Ожидаем загрузки страницы
        time.sleep(5)

        # Нажимаем на кнопку воспроизведения

    else:
        # Если запрос пустой, выводим сообщение об ошибке
        print("Запрос не распознан")


def get_wifi_password():
    speak("Введите название сети, к паролю которой вы хотите получить доступ")
    profile_name = input("Название сети: ")

    # Формируем команду и запускаем ее с помощью os.system
    command = f'netsh wlan show profiles name="{profile_name}" key=clear'
    output = os.popen(command).read()

    # Ищем пароль в выводе команды
    password = None
    for line in output.split("\n"):
        if "Key Content" in line:
            password = line.split(":")[-1].strip()
            break

    # Выводим найденный пароль
    if password:
        print(f"Пароль для сети '{profile_name}': {password}")
        speak(f"Пароль для сети '{profile_name}' это: {password}")

    else:
        speak(f"Пароль для сети не найден")
        print(f"Пароль для сети '{profile_name}' не найден")


def get_weather_data(city, api_key):
    weather_response = requests.get(weather_url.format(city, api_key))
    weather_data = json.loads(weather_response.text)
    return weather_data

def get_news(topic):
    # URL новостного сайта
    url = f'https://www.google.com/search?q={topic}&source=lnms&tbm=nws'

    # Получение HTML-кода страницы
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Извлечение заголовков новостей и их языка
    news_list = soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd')
    headlines = []
    for news in news_list:
        title = news.text
        language = detect_language(title)
        headline = {"title": title, "language": language}
        headlines.append(headline)

    return headlines


def detect_language(text):
    detector = langdetect.detect_langs(text)
    if len(detector) > 0:
        lang = str(detector[0]).split(':')[0]
        return lang
    else:
        return 'unknown'


def get_weather(city, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city

    try:
        response = requests.get(complete_url)
        data = response.json()
        if data["cod"] != "404":
            return data
        else:
            return None
    except:
        return None



translations = {
        "clear sky": "ясное небо",
        "few clouds": "небольшая облачность",
        "scattered clouds": "облачно с прояснениями",
        "broken clouds": "облачно с прояснениями",
        "overcast clouds": "пасмурно",
        "light rain": "небольшой дождь",
        "moderate rain": "умеренный дождь",
        "heavy intensity rain": "сильный дождь",
        # Добавьте другие переводы здесь
}

reminder_set = False

def set_reminder():
    global reminder_set
    speak("Когда вы хотите установить напоминание? (в формате ЧЧ:ММ) ")

    qu = recognize_speech().replace(" ", ":")

    speak("Что вам напомнить? ")
    qut = recognize_speech()
    speak(f"Установлено напоминание на {qu} для {qut}")
    reminder_set = True
    while True:
        current_time = time.strftime("%H:%M")
        if current_time == qu:
            speak(f"Напоминание: {qut}")
            # проигрывание звукового сигнала
            frequency = 2500  # частота звука
            duration = 1000  # длительность звука
            winsound.Beep(frequency, duration)
            reminder_set = False
            break
        time.sleep(20)  # проверка времени каждую минуту

# запуск функции напоминания в отдельном потоке

# Запускаем цикл работы ассистента в фоновом режиме
while True:
    # Распознаем речь
        if reminder_set:
            time.sleep(0)
            continue
        query = recognize_speech()
        # Обрабатываем запрос
        if "поисковая строка" in query or "поисковую строку" in query:
            keyboard.press_and_release('Ctrl+L')
            speak("поисковая строка активирована")
        elif "новости" in query.lower():

            news = get_news(query)
            for headline in news:
                if "uk" in headline["language"]:
                    continue
                print(headline)
                speak(headline["title"])
                if "description" in headline:
                    if "uk" in headline["language"]:
                        speak("Извините, описание новости доступно только на украинском языке.")
                    else:
                        speak(headline["description"])
            speak("Это все свежие новости по запросу " + query)

        elif "создай напоминание" in query:

            reminder_thread = threading.Thread(target=set_reminder)
            reminder_thread.start()
        elif "введи" in query:
            search_term = re.search('введи (.+)', query)
            if search_term:
                search_term = search_term.group(1).replace(' ', '_')
                keyboard.write(search_term)
            # запрашиваем новый запрос и вводим его в адресную строку
                keyboard.press_and_release('enter')
        elif "привет" in query:
            if 4 <= current_time.hour < 12:
                greetings = ["Доброе утро", "Утречка", "Доброго времени суток", "Здраствуйте"]
                speak(random.choice(greetings))
            elif 12 <= current_time.hour < 16:
                greeting = ["Добрый день", "Приветствую", "Доброго времени суток", "Здраствуйте"]
                speak(random.choice(greeting))
            elif 16 <= current_time.hour < 23:
                greets = ["Добрый вечер", "Как поживаете?", "Доброго времени суток", "Здраствуйте"]
                speak(random.choice(greets))
            else:
                speak("Доброй ночи" or "Сейчас познее время, лучше поспите")

        elif "доброго дня" in query or "добрый день" in query or "добрый вечер" in query or "доброго вечера" in query or "доброго утра" in query or "доброе утро" in query:
            if 4 <= current_time.hour < 12:
                speak("Доброе утро")
            elif 12 <= current_time.hour < 16:
                speak("Добрый день")
            elif 16 <= current_time.hour < 22:
                speak("Добрый вечер")
            else:
                speak("Доброй ночи")


        elif "как дела" in query:
            list = ["Отлично! А у вас?", "Супер", "Хороший вопрос. Надо будет это обдумать"]
            speak(random.choice(list))
        elif "открой браузер" in query:
            webbrowser.open("https://www.chrome.com")
            speak("Открываю Гугл Хром")
        elif "выключись" in query:
            speak("До свидания!")
            break
        elif "пока" in query:
            list = ["До свидания!", "хорошего вам дня"]
            speak(random.choice(list))

            break
        elif "скоро увидимся" in query:
            list = ["До свидания!", "хорошего вам дня", "до встречи"]
            speak(random.choice(list))
            break
        elif "сколько времени" in query or "сколько сейчас времени" in query or "который час" in query or "который сейчас час" in query:
            current_time = datetime.datetime.now().strftime("%H:%M")
            speak(f"Сейчас {current_time}")
        elif "какой сегодня день" in query:
            MONTH_NAMES = {
                1: 'января',
                2: 'февраля',
                3: 'марта',
                4: 'апреля',
                5: 'мая',
                6: 'июня',
                7: 'июля',
                8: 'августа',
                9: 'сентября',
                10: 'октября',
                11: 'ноября',
                12: 'декабря'
            }
            now = datetime.datetime.now()
            day = now.day
            month = MONTH_NAMES[now.month]
            year = now.year
            speak(f"Сегодня {day} {month} {year} года")



        elif "повтори за мной" in query:
            text = re.search('повтори за мной (.+)', query).group(1)
            speak(text)
        elif "повтори" in query:
            text = re.search('повтори (.+)', query).group(1)
            speak(text)
        # открываем новую вкладку
        elif "полноэкранный режим" in query:
            time.sleep(2)  # ждем 2 секунды
            pyautogui.press('f')




        elif "полноэкранного режима" in query:
            keyboard.press_and_release('f')
        elif "субтитры" in query:
            keyboard.press_and_release('c')


        elif "открой новую вкладку" in query:
            keyboard.press_and_release('ctrl+t')
        elif "открой три вкладки" in query:
            keyboard.press_and_release('ctrl+t')
            keyboard.press_and_release('ctrl+t')
            keyboard.press_and_release('ctrl+t')
        elif "закрой браузер" in query:
            os.system("taskkill /im chrome.exe /f")
        # переключаемся на следующую вкладку
        elif "следующая вкладка" in query:
            keyboard.press_and_release('ctrl+tab')
        # переключаемся на предыдущую вкладку

        elif "следующую вкладку" in query or "следующую страницу" in query or "следующей вкладке" in query or "следующей странице" in query:
            keyboard.press_and_release('ctrl+tab')
        # переключаемся на предыдущую вкладку
        elif "предыдущую вкладку" in query or "предыдущую страницу" in query or "предыдущей вкладке" in query or "предыдущей страницу" in query or "предыдущая вкладка" in query or "предыдущая страница" in query:
            keyboard.press_and_release('ctrl+shift+tab')

        # закрываем текущую вкладку
        elif "закрой вкладку" in query or "закрой страницу" in query:
            keyboard.press_and_release('ctrl+w')
        elif "википедия" in query:
            search_term = re.search('википедия (.+)', query)
            if search_term:
                search_term = search_term.group(1).replace(' ', '_')

                wiki_url = f"https://ru.wikipedia.org/wiki/{search_term}"

                webbrowser.open(wiki_url)
        elif "закрой две вкладки" in query:
            speak("закрываю вкладки")
            keyboard.press_and_release('ctrl+w')
            time.sleep(1)
            keyboard.press_and_release('ctrl+w')

        elif "закрой три вкладки" in query:
            speak("закрываю вкладки")
            keyboard.press_and_release('ctrl+w')
            time.sleep(1)
            keyboard.press_and_release('ctrl+w')
            time.sleep(1)
            keyboard.press_and_release('ctrl+w')
        elif "закрой четыре вкладки" in query:
            speak("закрываю вкладки")
            keyboard.press_and_release('ctrl+w')
            time.sleep(1)
            keyboard.press_and_release('ctrl+w')
            time.sleep(1)
            keyboard.press_and_release('ctrl+w')
            time.sleep(1)
            keyboard.press_and_release('ctrl+w')
        elif "закрой пять вкладок" in query:
            speak("закрываю вкладки")
            keyboard.press_and_release('ctrl+w')
            time.sleep(1)
            keyboard.press_and_release('ctrl+w')
            time.sleep(1)
            keyboard.press_and_release('ctrl+w')
            time.sleep(1)
            keyboard.press_and_release('ctrl+w')
            time.sleep(1)
            keyboard.press_and_release('ctrl+w')
        elif "закрой одну вкладку" in query:
            speak("закрываю вкладку")
            keyboard.press_and_release('ctrl+w')
            speak("закрываю вкладку")
        elif "википедии" in query:
            search_term = re.search('википедия (.+)', query)
            if search_term:
                search_term = search_term.group(1).replace(' ', '_')

                wiki_url = f"https://ru.wikipedia.org/wiki/{search_term}"

                webbrowser.open(wiki_url)

        elif "открой фильм" in query or "включи фильм" in query:
            k_url = "https://kinokong.pro/filmes/"
            speak("Открываю сайт в котором вы сможете найти фильм на любой вкус")
            webbrowser.open(k_url)


        elif "сделай ярче" in query or "повысь яркость" in query or "увеличь яркость" in query or "подними яркость" in query:
            brightness = wmi.WMI(namespace='wmi').WmiMonitorBrightness()[0].CurrentBrightness  # получаем текущую яркость
            new_brightness = int(min(brightness + 20, 100))  # умножаем на 1.1 и округляем до целого числа
            wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(new_brightness, 0)  # устанавливаем новую яркость

            speak("Яркость повышена")
        elif "сделай тусклее" in query or "понизь яркость" in query or "уменьши яркость" in query or "уменьш яркость" in query or "опусти яркость" in query:
                # Получаем текущую яркость экрана
            current_brightness = wmi.WMI(namespace='wmi').WmiMonitorBrightness()[0].CurrentBrightness

            # Вычисляем новое значение яркости (уменьшаем на 10%)
            new_brightness = max(1, current_brightness - int(255 * 0.1))

            # Устанавливаем новое значение яркости экрана
            wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(new_brightness, 0)
            speak("Яркость понижена")
        elif "включи видео" in query or "открой видео" in query or "запусти видео" in query or "найди видео" in query:

            play_video()




        elif "кто ты" in query:
            speak("Я голосовой помощник Stella")
            print("Я голосовой помощник Stella")
        elif "как тебя зовут" in query:
            speak("Меня зовут Stella")
            print("Меня зовут Stella")
        elif "стелла" in query or "стела" in query:
            list = ["слушаю", "что прикажете", "я сдесь", "не волнуйтесь,,,не сбежала", "к вашим услугам"]
            speak(random.choice(list))

        elif "что ты умеешь" in query:
            speak("Мои возможности не очень велики, но вот список всего что я умею.... Говорить погоду, время и новости, также могу рассказать анекдот, управлять яркостью экрана, открывать видео по вашему запросу, могу открывать ворд, эксель, паверпойнт, блокнот, медиаплеер и браузер, также можете сказать открой сайт ютуб или другие, в моих возможностях сказать имя пользователя, количество ядер и операционную систему устройства.. Вбраузере я могу переключатся между вкладками, создавать и удалять их, также я могу открывать историю браузера, параметры устройства и панель управления,,,.. и это только часть моих возможностей ")

        elif "погода на" in query:

            search_term = re.search('погод на (.+) в (.+)', query.rstrip('е'))

            translations = {

                "clear sky": "ясное небо",

                "few clouds": "небольшая облачность",

                "scattered clouds": "облачно с прояснениями",

                "broken clouds": "облачно с прояснениями",

                "overcast clouds": "пасмурно",

                "light rain": "небольшой дождь",

                "moderate rain": "умеренный дождь",

                "heavy intensity rain": "сильный дождь",

                # Добавьте другие переводы здесь

            }

            if search_term:

                day = search_term.group(1)

                if day == 'сегодня':

                    date = datetime.date.today().strftime('%Y-%m-%d')

                else:

                    date = day

                city = search_term.group(2).replace(' ', '_')

                print(f"Вы хотите узнать погоду в городе {city} на {day}")

                weather_data = get_weather(city, api_key)

                if weather_data:

                    description = weather_data['weather'][0]['description']

                    # Находим соответствующий перевод в словаре

                    if description in translations:

                        translated_description = translations[description]

                    else:

                        # Если перевод не найден, используем описание на английском языке

                        translated_description = description

                    temperature = int(weather_data['main']['temp'] - 273.15)

                    humidity = weather_data['main']['humidity']

                    wind_speed = weather_data['wind']['speed']

                    speak(
                        f"В городе {city} на {day} будет {translated_description}, температура {temperature} градусов Цельсия, влажность {humidity} процентов, скорость ветра {wind_speed} метров в секунду.")
                    # Создаем словарь соответствия описания погоды и рекомендуемой одежды/активностей
                    weather_recommendations = {
                        "ясное небо": "Оденьтесь легко и возьмите солнцезащитные очки. Можете отправиться на пикник или на прогулку в парк.",
                        "небольшая облачность": "Оденьтесь потеплее и возьмите зонт на случай дождя. Хорошо подходит для прогулок.",
                        "облачно с прояснениями": "Оденьтесь потеплее и возьмите зонт на случай дождя. Можете отправиться на прогулку.",
                        "пасмурно": "Оденьтесь потеплее и возьмите зонт на случай дождя. Рекомендуется оставаться дома.",
                        "небольшой дождь": "Оденьтесь потеплее и возьмите зонт. Рекомендуется оставаться дома.",
                        "умеренный дождь": "Оденьтесь потеплее и возьмите зонт. Рекомендуется оставаться дома.",
                        "сильный дождь": "Оденьтесь потеплее и возьмите зонт. Рекомендуется оставаться дома.",
                        # Добавьте другие рекомендации здесь
                    }

                    # Находим соответствующую рекомендацию в словаре
                    if description in weather_recommendations:
                        recommendations = weather_recommendations[description]
                    else:
                        # Если рекомендация не найдена, используем общие рекомендации для погоды
                        recommendations = "Оденьтесь соответственно погоде и выберите активность в соответствии с вашими интересами."
                    speak(f"Для такой погоды я бы рекомендовала: {recommendations}")

                else:

                    speak("Извините, не удалось получить данные о погоде. Возможно ошибка в сказанном вами городе. Попробуйте сказать например.. Какая погода на завтра в Киеве")


            else:

                speak("Извините, я не понимаю, о каком городе и дне вы говорите.")


        elif "погода в" in query:

            search_term = re.search('погода в (.+) на (.+)', query)

            translations = {

                "clear sky": "ясное небо",

                "few clouds": "небольшая облачность",

                "scattered clouds": "облачно с прояснениями",

                "broken clouds": "облачно с прояснениями",

                "overcast clouds": "пасмурно",

                "light rain": "небольшой дождь",

                "moderate rain": "умеренный дождь",

                "heavy intensity rain": "сильный дождь",

                # Добавьте другие переводы здесь

            }

            if search_term:

                city = search_term.group(1).rstrip('е').replace(' ', '_')

                day = search_term.group(2)

                if day == 'сегодня':

                    date = datetime.date.today().strftime('%Y-%m-%d')

                else:

                    date = day

                print(f"Вы хотите узнать погоду в городе {city} на {day}")

                weather_data = get_weather(city, api_key)

                if weather_data:

                    description = weather_data['weather'][0]['description']

                    # Находим соответствующий перевод в словаре

                    if description in translations:

                        translated_description = translations[description]

                    else:

                        # Если перевод не найден, используем описание на английском языке

                        translated_description = description

                    temperature = int(weather_data['main']['temp'] - 273.15)

                    humidity = weather_data['main']['humidity']

                    wind_speed = weather_data['wind']['speed']

                    speak(
                        f"В городе {city} на {day} будет {translated_description}, температура {temperature} градусов Цельсия, влажность {humidity} процентов, скорость ветра {wind_speed} метров в секунду.")

                    # Создаем словарь соответствия описания погоды и рекомендуемой одежды/активностей
                    weather_recommendations = {
                        "ясное небо": "Оденьтесь легко и возьмите солнцезащитные очки. Можете отправиться на пикник или на прогулку в парк.",
                        "небольшая облачность": "Оденьтесь потеплее и возьмите зонт на случай дождя. Хорошо подходит для прогулок.",
                        "облачно с прояснениями": "Оденьтесь потеплее и возьмите зонт на случай дождя. Можете отправиться на прогулку.",
                        "пасмурно": "Оденьтесь потеплее и возьмите зонт на случай дождя. Рекомендуется оставаться дома.",
                        "небольшой дождь": "Оденьтесь потеплее и возьмите зонт. Рекомендуется оставаться дома.",
                        "умеренный дождь": "Оденьтесь потеплее и возьмите зонт. Рекомендуется оставаться дома.",
                        "сильный дождь": "Оденьтесь потеплее и возьмите зонт. Рекомендуется оставаться дома.",
                        # Добавьте другие рекомендации здесь
                    }

                    # Находим соответствующую рекомендацию в словаре
                    if description in weather_recommendations:
                        recommendations = weather_recommendations[description]
                    else:
                        # Если рекомендация не найдена, используем общие рекомендации для погоды
                        recommendations = "Оденьтесь соответственно погоде и выберите активность в соответствии с вашими интересами."

                    # Выводим рекомендации по одежде и активностям
                    speak(f"Для такой погоды я бы рекомендовала: {recommendations}")

                else:

                    speak("Извините, не удалось получить данные о погоде. Возможно ошибка в сказанном вами городе")


            else:

                speak("Извините, я не понимаю, о каком городе и дне вы говорите.")

        elif "погода" in query or "погоду" in query:

            speak("В каком городе узнать погоду?")

            try:

                with sr.Microphone() as source:

                    r.adjust_for_ambient_noise(source)

                    audio = r.listen(source)

                city = r.recognize_google(audio, language="ru-RU")

                print("Вы сказали: " + city)

                weather_response = requests.get(weather_url.format(city, api_key))

                weather_data = json.loads(weather_response.text)

                if weather_data.get("cod") == 200:

                    description = weather_data['weather'][0]['description']

                    temperature = int(weather_data['main']['temp'] - 273.15)

                    humidity = weather_data['main']['humidity']

                    wind_speed = weather_data['wind']['speed']

                    speak(
                        f"Сейчас в городе {city} {description}, температура {temperature} градусов Цельсия, влажность {humidity} процентов, скорость ветра {wind_speed} метров в секунду.")

                else:

                    speak("Извините, не удалось получить данные о погоде. Возможно ошибка в сказанном вами городе")

            except sr.UnknownValueError:

                speak("Извините, я не понимаю, какой город вы назвали.")


        elif "поиск" in query or "найди" in query or "поищи" in query:
            search_in_browser()


        elif "далее" in query or "enter" in query or "дальше" in query:
            keyboard.press_and_release('enter')


        elif "обнови запрос" in query:
            # выделяем адресную строку и удаляем текст
            keyboard.press_and_release('ctrl+l')
            keyboard.press_and_release('ctrl+a')
            keyboard.press_and_release('delete')

            # запрашиваем новый запрос и вводим его в адресную строку
            speak("Скажите ваш запрос:")
            query = recognize_speech()
            keyboard.write(query)
            keyboard.press_and_release('enter')

        elif "пауза" in query:
            play_pause()

        elif "перемотай видео вперёд" in query or "перемотай вперёд" in query or "видео вперёд" in query:
            next_video()
        elif "перемотай видео назад" in query or "перемотай назад" in query or "видео назад" in query:
            previous_video()



        elif "страницу загрузок" in query or "страница загрузок" in query or "открой загрузки" in query or "страница загрузок" in query:
            keyboard.press_and_release('ctrl+j')
            speak("открываю страницу загрузок")

        elif "открой историю" in query:
            keyboard.press_and_release('ctrl+h')

        elif "закрывшуюся вкладку" in query or "верни вкладку" in query:
            keyboard.press_and_release('Ctrl+Shift+T')

        elif "сохранить" in query or "сохрани" in query:
            keyboard.press_and_release('Ctrl+S')
            speak("кнопка сохранить нажата")
        elif "копировать" in query or "копируй" in query or "скопируй" in query:
            keyboard.press_and_release('Ctrl+C')
            speak("кнопка копировать нажата")
        elif "вставить" in query or "вставь" in query:
            keyboard.press_and_release('Ctrl+V')
            speak("кнопка вставить нажата")

        elif "панель поиска" in query:
            keyboard.press_and_release('Ctrl+F')
            speak("Панель поиска открыта")
        elif "повтори отмененное действие" in query or "повторить отмененное действие" in query:
            keyboard.press_and_release('Ctrl+Y')
        elif "закрой все окна" in query or "закрой окна" in query:
            keyboard.press_and_release('Win+D')


        elif "панель управления" in query:
            os.system("control")
            time.sleep(1)
            speak("панель управления открыта")
        elif "включи параметры" in query:
            keyboard.press_and_release('Win+I')
            time.sleep(1)
            speak("параметры открыты")
        elif "открой параметры" in query:
            keyboard.press_and_release('Win+I')
            time.sleep(1)
            speak("параметри открыты")

        elif "открой блокнот" in query or "запусти блокнот" in query:
            os.system("notepad.exe")
        elif "закрой блокнот" in query:
            os.system("taskkill /im notepad.exe /f")
        elif "открой медиаплеер" in query or "открой плеер" in query or "запусти медиаплеер" in query or "запусти плеер" in query:
            os.system("mediaplayer.exe")
        elif "закрой медиаплеер" in query or "закрой плеер" in query:
            os.system("taskkill /im mediaplayer.exe /f")
        elif "включи музыку" in query or "включи песни" in query or "включи песню" in query:
            os.system("mediaplayer.exe")
            speak("открываю медиаплеер, где вы сможете включить любимую музыку")

        elif "перезагрузи" in query:
            os.system("shutdown -r -t 5")
            speak("Устройство будет перезагружено через 5 секунд.")
        elif "выключи" in query:
            os.system("shutdown -s -t 5")
            speak("Устройство будет выключено через 5 секунд.")



        elif "пароль от вайфай" in query or "пароль от wi-fi" in query or "пароль вайфай" in query or "пароль wi-fi" in query:

            get_wifi_password()

        elif "расскажи шутку" in query or "расскажи анекдот" in query:
            list = ["Бабушка две недели играла с внуком в школу. К концу второй недели она узнала, что делает за него домашнее задание", "Вчера моя бабуля, увидев, как я говорю с друзьями по скайпу, пошла говорить с президентом по телевизору", "Хорошего бухгалтера найти трудно, поэтому Вера Павловна уже двадцать лет числится в розыске", "Судья выносит обвиняемому приговор — 25 лет. Обвиняемый: — Да вы что, мне же 83 года! Судья: — Мы не требуем от вас невозможного — отсидите, сколько сможете", "По радио передают новости: — В США два месяца назад был задержан злостный хакер Вася Иванов. Суд приговорил его к 10 годам тюремного заключения. По данным центрального полицейского компьютера США, завтра Вася Иванов выходит на свободу, полностью отбыв весь срок заключения", "Наблюдала картину, как ругаются глухонемые. Я, конечно, всё понимаю, но со стороны это выглядело более чем эпично, потому что для того, чтобы перебить оппонента, они бьют друг друга по рукам", " Клиент спрашивает у известного адвоката: Месье, если я заплачу вам одну тысячу евро, вы ответите мне на два вопроса? Адвокат отвечает: Конечно, уважаемый. А какой второй вопрос?"]
            speak(random.choice(list))



        elif "текущая директория" in query or "текущую директорию" in query or "данную директорию" in query:
            current_dir = os.getcwd()
            speak(current_dir)
            print(current_dir)


        elif "операционная система" in query:
            print(os.name)
            speak("Название вашей операционной системы" + os.name)
        elif "операционную систему" in query:
            print(os.name)
            speak("Название вашей операционной системы" + os.name)



        elif "мои координаты" in query:

            g = geocoder.ip('me')

            if g.ok:

                lat, lng = g.latlng

                speak(f"Ваши координаты: широта {lat} и долгота {lng}")

                print(f"Ваши координаты: широта {lat} и долгота {lng}")

            else:

                speak("Не удалось определить ваши координаты")

        elif any(x in query for x in ["скажи координаты", "узнай координаты", "назови координаты"]):

            search_term = re.search('(скажи|узнай|назови) координаты (.+)', query)

            if search_term:

                search_term = search_term.group(2).replace(' ', '_')

                location = geocoder.osm(search_term)

                if location.ok:

                    lat, lng = location.latlng

                    speak(f"Координаты местоположения {location.address}: широта {lat}, долгота {lng}")

                    print(f"Координаты местоположения {location.address}: широта {lat}, долгота {lng}")

                else:

                    speak("Не удалось найти координаты для указанного местоположения")

        elif "координаты" in query or "где находится" in query or "местонахождение" in query:

            search_term = re.search('(координаты|где находится|местонахождение) (.+)', query)

            if search_term:

                search_term = search_term.group(2).replace(' ', '_')

                location = geocoder.osm(search_term)

                if location.ok:

                    lat, lng = location.latlng

                    speak(f"Местоположение {location.address}. Координаты широты {lat} и долготы {lng}")

                    print(f"Местоположение {location.address}. Координаты широты {lat} и долготы {lng}")

                else:

                    speak("Не удалось найти координаты для указанного местоположения")




        elif "отключи wifi" in query or "отключи wi-fi" in query or "выключи wi-fi" in query or "выключи вайфай" in query:
            speak("идёт отключение вайвай" or "выключаю вайфай")
            os.system('ipconfig/release')
            speak("вайфай отключен")
            speak("  Сейчас я вынуждена выключится, поскольку не могу работать без вайфай. Хорошего вам дня")
            break


        elif "скажи имя пользователя" in query or "имя пользователя системы" in query or "назови имя пользователя" in query:
            username = os.getlogin()
            print(username)
            speak(username)



        elif "количество ядер" in query or "сколько ядер" in query:
            num_cores = os.cpu_count()
            print(num_cores)
            speak(num_cores)

        elif "открой ворд" in query:
            try:
                os.startfile('winword')
            except FileNotFoundError:
                pass  # Пропускаем команду, если соответствующее приложение не установлено

        elif "открой word" in query:
            try:
                os.startfile('winword')
            except FileNotFoundError:
                pass  # Пропускаем команду, если соответствующее приложение не установлено
                speak("У вас не установлен ворд")
        elif "открой ексель" in query or "открой exel" in query:
            try:
                os.startfile('excel')
            except FileNotFoundError:
                pass  # Пропускаем команду, если соответствующее приложение не установлено
                speak("У вас не установлен ексель")
        elif "открой поверпойнт" in query or "открой powerpoint" in query:
            try:
                os.startfile('powerpnt')
            except FileNotFoundError:
                pass  # Пропускаем команду, если соответствующее приложение не установлено
                speak("У вас не установлен паверпойнт")


        # Закрытие приложения Word
        elif "закрой ворд" in query or "закрой word" in query:
            try:
                os.system("TASKKILL /F /IM WINWORD.EXE")
            except FileNotFoundError:
                pass  # Пропускаем команду, если соответствующее приложение не установлено
                speak("У вас не установлен ворд")
        # Закрытие приложения Excel
        elif "закрой ексель" in query or "закрой excel" in query:
            try:
                os.system("TASKKILL /F /IM EXCEL.EXE")
            except FileNotFoundError:
                pass  # Пропускаем команду, если соответствующее приложение не установлено
                speak("У вас не установлен ексель")
        # Закрытие приложения PowerPoint
        elif "закрой поверпойнт" in query or "закрой powerpoint" in query:
            try:
                os.system("TASKKILL /F /IM POWERPNT.EXE")
            except FileNotFoundError:
                speak("У вас не установлен паверпойнт")
                pass  # Пропускаем команду, если соответствующее приложение не установлено





        elif "открой сайт" in query:

            # код для открытия приложения или файла
            search_term = re.search('открой (.+)', query)
            if search_term:
                search_term = search_term.group(1).replace(' ', '_')

                iki_url = f"https://{search_term}.com"
                speak(f'открываю {search_term}')
                webbrowser.open(iki_url)
        elif "отмена" in query:
            keyboard.press_and_release('Ctrl+Z')
            keyboard.press_and_release('esc')
            speak("действие отменено")
        elif "отмени" in query:
            keyboard.press_and_release('Ctrl+Z')
            keyboard.press_and_release('esc')
            speak("действие отменено")



        elif "кто такой" in query or "кто такая" in query or "что такое" in query or "кем" in query:

            wikipedia.set_lang("ru")

            try:

                page = wikipedia.page(query)

                summary = page.content.split('\n')[0]

                summary = re.sub(r'\([^)]*\)', '', summary)  # исключаем текст в скобках

                speak(summary)

            except wikipedia.exceptions.DisambiguationError as e:

                print(f"Слишком много возможных определений для запроса \"{query}\". Попробуйте уточнить запрос.")

            except wikipedia.exceptions.PageError as e:

                print(f"Не найдено статей, соответствующих запросу \"{query}\".")

            except Exception as e:

                print(f"Произошла ошибка: {e}")


        elif "скажи" in query:
            text = re.search('скажи (.+)', query)
            if text:
                text = text.group(1)
                speak(text)

