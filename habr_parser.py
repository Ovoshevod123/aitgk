from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from collections import Counter

# from AI_TGK.deepseek_test import ds, ds_2
from AI_TGK.gigachat import giga, giga_2
from AI_TGK.promts import promt_2, promt_3, promt_habr_1

data = {}
titles = []

# Настройка браузера
ua = dict(DesiredCapabilities.CHROME)
options = ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
driver = webdriver.Chrome(options=options)

def pars_news(promt):
    global data
    data.clear()
    titles.clear()

    for i in range(2):
        driver.get(f'https://habr.com/ru/news/page{i+1}/')
        # Парсим блок с новостями
        el = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'tm-page__main')))

        # Парсим по отдельности новости
        els = el.find_elements(By.TAG_NAME, 'article')

        # Находим и сохраняем заголовки и ссылки новостей
        for i in els:
            try:
                title = i.find_element(By.TAG_NAME, 'h2')
                href = title.find_element(By.TAG_NAME, 'a').get_attribute('href')
                text = i.find_element(By.TAG_NAME, 'p').text

                data[title.text] = {"href": href,
                                    "text": text}
            except:
                pass

        for i in data:
            promt += (f'{i} \n')
                      # f'{data[i]["text"]}\n\n')

    return promt

def titles_sort(promt):
    global data, titles
    # Просим нейросеть отобрать самые подходящие заголовки новостей на сегодня
    # for num in range(1):
    #     gpt = giga_2(promt)
    #     # gpt = ds_2(promt)
    #
    #     #Проверяем список заголовков со списком нейросети и сохраняем сходства в отдельный список
    #     for i in data:
    #         if i in gpt:
    #             titles.append(i)

    for i in data:
        titles.append(i)

    return titles

def parser_article(href):
    driver.get(href)
    body = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'post-content-body')))
    imgs = body.find_elements(By.TAG_NAME, 'img')

    gpt = giga(promt_2 + body.text)
    imgs = [i.get_attribute('src') for i in imgs]

    article = {
        "text": gpt,
        "imgs": imgs,
        "href": href
    }

    return article

def main():
    promt = pars_news(promt_habr_1)
    titles = titles_sort(promt)

if __name__ == "__main__":
    main()