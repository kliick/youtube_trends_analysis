import requests
import pandas as pd
import datetime


API_KEY = "AIzaSyCYmG9Ft6FRKN_Kc-le5yevDeF-We6mKe8"
VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
CATEGORY_URL = "https://www.googleapis.com/youtube/v3/videoCategories"


# Функция для загрузки категорий видео
def get_categories():
    params = {"part": "snippet", "regionCode": "RU", "key": API_KEY}
    response = requests.get(CATEGORY_URL, params=params).json()
    return {item["id"]: item["snippet"]["title"] for item in response["items"]}


# Функция для получения трендовых видео
def get_trending_videos(category_dict):
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": "RU",
        "maxResults": 50,
        "key": API_KEY
    }
    response = requests.get(VIDEO_URL, params=params).json()

    video_list = []
    for video in response["items"]:
        category_id = video["snippet"]["categoryId"]
        category_name = category_dict.get(category_id, "Unknown")

        video_list.append({
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "title": video["snippet"]["title"],
            "channel": video["snippet"]["channelTitle"],
            "category": category_name,
            "views": int(video["statistics"].get("viewCount", 0)),
            "likes": int(video["statistics"].get("likeCount", 0)),
            "comments": int(video["statistics"].get("commentCount", 0)),
            "publishedAt": video["snippet"]["publishedAt"]
        })
    return pd.DataFrame(video_list)


# Функция для сохранения новых данных в CSV
def save_data():
    category_dict = get_categories()
    df_new = get_trending_videos(category_dict)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    try:
        df_old = pd.read_csv("/Users/sergegribo/Desktop/ML/"
                             "portfolio/Youtube_trends/youtube_trends.csv")
        last_date = df_old["date"].max()
        if last_date == today:
            print("Данные за сегодня уже есть. Обновление не требуется.")
            return
        df = pd.concat([df_old, df_new], ignore_index=True)
    except FileNotFoundError:
        df = df_new

    df.to_csv("/Users/sergegribo/Desktop/ML/portfolio/Youtube_trends/"
              "youtube_trends.csv", index=False, encoding="utf-8-sig")
    print(f"Данные за {today} добавлены!")


save_data()
