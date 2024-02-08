NASA_API_URL = "〇〇"
API_KEY = "〇〇"  # 実際のプロジェクトでは適切な方法で管理すること

# streamlit_app.py

import streamlit as st
import requests
import sqlite3
from datetime import date

# カスタムフォントのスタイルを定義するCSS
custom_font_style = """
    <style>
        div,p {
            font-family: 'Futura','ヒラギノ丸ゴ ProN', sans-serif;
        }
    </style>
"""

# スタイルを表示
st.write(custom_font_style, unsafe_allow_html=True)

# FastAPIのエンドポイント
FASTAPI_ENDPOINT = "http://localhost:8000/astronomy/"

# SQLiteデータベースの接続
conn = sqlite3.connect("favorites.db")
if conn:
    print("データベースに接続しました")
cursor = conn.cursor()


def get_astronomy_data(date):
    params = {
        'api_key': API_KEY,
        'date': date
    }
    response = requests.get(NASA_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def load_favorite_data():
    cursor.execute("SELECT * FROM favorites")
    return cursor.fetchall()

def main():
    st.title("天体観測アプリ")

    # サイドバーにカレンダーを表示
    selected_date = st.sidebar.date_input("観測データの日付", date.today())

    if st.sidebar.button("観測データ取得"):
        # 選択された日付の天体データを取得
        formatted_date = selected_date.strftime("%Y-%m-%d")
        astronomy_data = get_astronomy_data(formatted_date)

        # データを表示
        if astronomy_data:
            st.write("天体データ:", astronomy_data)
            st.image(astronomy_data["url"], caption=f"Date: {astronomy_data['date']}", use_column_width=True)
            st.write(f"説明: {astronomy_data['explanation']}")


if __name__ == "__main__":
    main()
