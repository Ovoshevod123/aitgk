import requests
import uuid
import json

# 1. Аутентификация для получения токена
def get_access_token():
  Authorization_key = "Yzc0Y2NlZjItMGJlZS00YjVkLTk0N2UtYWY4ZjZhNDIxMmE0OjRjZWUxYjY5LWQ2NWUtNDY0MS05Y2I3LTdjNjRlZWMzMWVjYw=="

  url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

  headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
    "RqUID": str(uuid.uuid4()),  # Уникальный ID запроса
    "Authorization": f"Basic {Authorization_key}"
  }
  data = {"scope": "GIGACHAT_API_PERS"}  # Необходимый уровень доступа

  response = requests.post(url, headers=headers, data=data, verify=False)
  try:
    return response.json()['access_token']
  except:
    print(response.json())

def get_req(token, promt):
  url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

  payload = json.dumps({
    "model": "GigaChat",
    "messages": [
      {
        "role": "user",
        "content": promt
      }
    ],
    "stream": False,
    "repetition_penalty": 1
  })
  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {token}'}
  response = requests.request("POST", url, headers=headers, data=payload, verify=False)

  req = response.json()
  return req['choices'][0]['message']['content']

def giga(promt):
  return get_req(token=get_access_token(), promt=promt)

def giga_2(promt):
  return """Будущее без Google Search? ИИ-помощники меняют привычки пользователей
Троян BrowserVenom замаскировали под DeepSeek для Windows
Sega подала множество заявок на регистрацию товарных знаков в России по Мадридскому протоколу
ТОП-5 ИБ-событий недели по версии Jet CSIRT
AMD выпустила бюджетный процессор Ryzen 5 5500X3D AM4 с 3D-кэшем
Reuters: Google планирует разорвать отношения со Scale AI
«Яндекс» выпустил отчёт об устойчивом развитии за 2024 год
Пять факторов, формирующих конкурентную среду на отечественном ИТ-рынке
За шесть лет Amazon инвестирует $13 млрд в дата-центры для развития ИИ в Австралии
Скам-тест: мошенники приглашают тестировщиков приложений, взламывают их устройства и похищают деньги
«Ванильный» K8s VS коммерческие решения: когда стоит платить?
Apple разрешит сторонним музыкальным сервисам показывать анимированные обложки на экране блокировки в iOS 26
Apple запланировала выпуск публичных бета-версий обновлений для AirPods
НАСА заморозило проект посадочного модуля для Европы и предлагает отправить его на Энцелад
Глава «Почты России» считает чрезмерной зарплату курьера в 300 тыс. рублей
Google и Microsoft планируют прекратить сотрудничество с Scale AI
Samsung сворачивает поддержку умных часов Galaxy на базе Tizen c сентября 2025 года
Ubisoft и Unfrozen отложили ранний доступ к игре Heroes of Might & Magic: Olden Era на конец 2025 года
Как ChatGPT может подтолкнуть к конспирологическому мышлению
YouTube тестирует 30-секундную рекламу на Smart TV и устройствах с Chromecast
Будущее без Google Search? ИИ-помощники меняют привычки пользователей
Троян BrowserVenom замаскировали под DeepSeek для Windows
Sega подала множество заявок на регистрацию товарных знаков в России по Мадридскому протоколу
ТОП-5 ИБ-событий недели по версии Jet CSIRT
AMD выпустила бюджетный процессор Ryzen 5 5500X3D AM4 с 3D-кэшем
Reuters: Google планирует разорвать отношения со Scale AI
«Яндекс» выпустил отчёт об устойчивом развитии за 2024 год
Пять факторов, формирующих конкурентную среду на отечественном ИТ-рынке
За шесть лет Amazon инвестирует $13 млрд в дата-центры для развития ИИ в Австралии
Скам-тест: мошенники приглашают тестировщиков приложений, взламывают их устройства и похищают деньги
«Ванильный» K8s VS коммерческие решения: когда стоит платить?
Apple разрешит сторонним музыкальным сервисам показывать анимированные обложки на экране блокировки в iOS 26
Apple запланировала выпуск публичных бета-версий обновлений для AirPods
НАСА заморозило проект посадочного модуля для Европы и предлагает отправить его на Энцелад
Глава «Почты России» считает чрезмерной зарплату курьера в 300 тыс. рублей
Google и Microsoft планируют прекратить сотрудничество с Scale AI
Samsung сворачивает поддержку умных часов Galaxy на базе Tizen c сентября 2025 года
Ubisoft и Unfrozen отложили ранний доступ к игре Heroes of Might & Magic: Olden Era на конец 2025 года
Как ChatGPT может подтолкнуть к конспирологическому мышлению
YouTube тестирует 30-секундную рекламу на Smart TV и устройствах с Chromecast
Тест CRMArena-Pro показывает, что ИИ-агенты испытывают трудности в реальных бизнес-задачах
В Windows 11 вернут часы в выпадающем календаре
Компания Mechanize создает цифровые офисы для обучения ИИ-агентов
Разработан первый в мире 2D-компьютер без использования кремния
Rednote выпускает свою первую языковую модель с открытым исходным кодом и архитектурой Mixture-of-Experts
Студии Ghibli — 40 лет, но её будущее оказалось под вопросом
Релиз кроссплатформенного открытого многофункционального архиватора PeaZip 10.5
nanoДРАЙВ в Уфе: российские цифровые решения для строительства и производства
Выпуск Cjam 1.9.9.0 — легковесного редактора MP3 для ПК на ОС Windows
Вышел бенчмарк для HDD и SSD CrystalDiskMark 9.0.0
Релиз CrystalDiskInfo 9.7.0
Китай присоединяется к США в гонке по внедрению имплантатов в мозг
Вышел выпуск открытого кроссплатформенного редактора схем и диаграмм qdia 0.53
Финал Национальной студенческой лиги киберспорта «Сбера» прошёл в Москве
Роскомнадзор: YouTube и Instagram** в России недоступны, оснований для снятия ограничений нет
Как устроены сети: от локальных до глобальных
ChatGPT o3 прошла Pokemon Red — но до человеческих игроков все равно далеко
Новый метод позволяет физически восстановить оригинальные картины с помощью цифровых плёнок
В Play Store появился эмулятор PS3 для Android
PS5 обогнала PS4 по количеству активных ежемесячных пользователей"""

# if __name__ == "__main__":
#   print(giga('fdsfa'))