import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from wordcloud import WordCloud
import plotly.express as px
import nltk
from nltk.corpus import stopwords


# Функция загрузки данных
@st.cache_data
def load_data():
    """Загружаем обновлённые данные из CSV и конвертируем дату"""
    df = pd.read_csv("youtube_trends.csv", parse_dates=["date"])
    return df


df = load_data()
st.title("Анализ трендов YouTube")

selected_date = st.sidebar.date_input("Выберите дату", df["date"].max())
df_filtered = df[df["date"] == str(selected_date)]

# Кнопка для обновления данных вручную
if st.button("Обновить данные"):
    st.rerun()

# 1.Динамика просмотров по датам
st.subheader("Динамика просмотров по датам")
df_views = df.groupby("date", as_index=False)["views"].sum()
fig = px.line(df_views, x="date", y="views", title="Динамика просмотров")
fig.update_xaxes(
    tickformat="%d-%m-%Y",
    tickangle=45,
    dtick="D1"
)
st.plotly_chart(fig)


# 2.Топ-10 видео по просмотрам
st.subheader(' ')
st.subheader(f"Топ-10 видео за {selected_date}")
st.dataframe(df_filtered.sort_values(by="views", ascending=False)[["title",
             "channel", "views"]].head(10))


# 3.Какие категории чаще попадают в тренды?
category_counts = df["category"].value_counts().reset_index()
category_counts.columns = ["category", "count"]
st.subheader(' ')
st.subheader("Какие категории видео чаще попадают в тренды?")
fig = px.bar(category_counts, x="category", y="count",
             title="Частота появления категорий в трендах",
             labels={"category": "Категория",
                     "count": "Количество видео в трендах"},
             text_auto=True)

fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig)


# 4.Популярные категории
st.subheader(' ')
st.subheader("Популярность категорий в трендах по дням")
df_category = df.groupby(["date", "category"]).size().reset_index(name="count")
fig = px.line(df_category, x="date", y="count", color="category",
              labels={"date": "Дата", "count": "Количество видео",
                      "category": "Категория"},
              markers=True)
fig.update_layout(
    xaxis=dict(tickformat="%d-%m-%Y"),
    legend=dict(title="Категории", orientation="h", yanchor="bottom", y=-0.7,
                xanchor="right", x=1),
)
st.plotly_chart(fig)


# 5.Продолжительность видео в трендах
video_trend_days = df.groupby("title")["date"].nunique().reset_index()
video_trend_days.rename(columns={"date": "trend_duration"}, inplace=True)
st.subheader(' ')
st.subheader("Продолжительность нахождения видео в трендах")
fig = px.histogram(video_trend_days, x="trend_duration", nbins=10,
                   title="Распределение длительности "
                         "нахождения видео в трендах",
                   labels={"trend_duration": "Количество дней в трендах"})
st.plotly_chart(fig)
df_categories = df[["title", "category"]].drop_duplicates()
video_trend_days = video_trend_days.merge(df_categories, on="title",
                                          how="left")
category_trend_duration = (
    video_trend_days.groupby("category")["trend_duration"]
    .mean()
    .reset_index()
    .sort_values(by="trend_duration", ascending=False)
)
st.subheader("Средняя продолжительность нахождения видео "
             "в трендах по категориям")
fig = px.bar(category_trend_duration, x="category", y="trend_duration",
             title="Средняя продолжительность видео в трендах",
             labels={"category": "Категория",
                     "trend_duration": "Среднее число дней"},
             text_auto=True)
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig)


# 6.Частотный анализ заголовков
st.subheader(' ')
st.subheader("Самые популярные слова в заголовках")
nltk.download('stopwords')
stop_words = set(stopwords.words('russian') + stopwords.words('english'))
df["clean_title"] = df["title"].apply(
    lambda x: re.sub(r"[^\w\s]", "", str(x).lower())
)
all_words = " ".join(df["clean_title"]).split()
for i in all_words:
    if i in stop_words:
        all_words.remove(i)
wordcloud = (
    WordCloud(width=800, height=400, background_color="white")
    .generate(" ".join(all_words))
)
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)


# 7.Зависимость между просмотрами, лайками и переменными
corr_data = df[["views", "likes", "comments"]]
corr_matrix = corr_data.corr()
st.subheader(" ")
st.subheader("Корреляция между просмотрами, лайками и комментариями")
fig, ax = plt.subplots(figsize=(5, 4))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f",
            linewidths=0.5, ax=ax)
st.pyplot(fig)


# 8.Самые частые каналы в трендах
st.subheader(' ')
st.subheader("Топ-10 каналов в трендах")
top_channels = df["channel"].value_counts().head(10)
st.bar_chart(top_channels)

st.write("**Проект по анализу трендов YouTube с "
         "автоматическим обновлением данных.**")
