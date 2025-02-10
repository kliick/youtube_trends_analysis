# Анализ трендов YouTube

Этот проект посвящён анализу трендов YouTube с использованием данных, полученных через YouTube API. Я исследовал, какие категории видео чаще попадают в тренды, как долго они остаются популярными и какие факторы могут влиять на их успех.


## Демо проекта

- 🔗 [Интерактивный дашборд на Streamlit](https://share.streamlit.io/ТВОЙ-ПРОЕКТ)
- ✍️ [Статья на Medium с подробным анализом](https://medium.com/ТВОЯ-СТАТЬЯ)


## Технологии и инструменты

- **Python** — для обработки данных и анализа
- **Pandas** — для работы с табличными данными
- **Plotly & Seaborn & Matplotlib** — для визуализации
- **Streamlit** — для создания интерактивного дашборда
- **YouTube API** — для сбора данных о трендах
- **Cron** — для автоматизации обновления данных
- **itertools** - для частотного анализа заголовков
- **wordcloud** - для визуализации частоты слов


## Как запустить проект
```bash
git clone https://github.com/kliick/youtube-trends-analysis.git
cd Youtube_trends
pip install -r requirements.txt
streamlit run app.py
```


## **Структура проекта**  
```markdown
## Структура проекта

Youtube_trends/
├──app.py                   #Код для Streamlit-дашборда
├──youtube_scraper.py       #Скрипт для сбора данных через YouTube API
├──youtube_trends.csv       #Собранные данные о трендах
├──requirements.txt         #Зависимости проекта
├──log.txt                  #Лог ежедневного выполнения скрипта (CronJob)
└── README.md               #Описание проекта



##
## Основные выводы
- **Entertainment**, **People & Blogs** и **Gaming** - самые популярные категории в трендах
- Видео остается в трендах в среднем **1–2 дня**, но бывают исключения
- Заголовки трендовых видео часто содержат слова **"shorts"** и **"vs"**, а также имеют заглавные буквы
- Просмотры и лайки сильно коррелируют **(0,91)**, тогда как комментарии и просмотры коррелируют умеренно **(0,56)**
- Тренды **практически не меняются**, в связи с чем преобладают почти одни и те же категории


Подробнее о результатах анализа в [Medium-статье](https://medium.com/ТВОЯ-СТАТЬЯ).
