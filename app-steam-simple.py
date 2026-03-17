import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Steam Dashboard", layout="wide")

st.title("📊 Steam Analytics Viz")
st.sidebar.header("Налаштування")

# Завантаження файлів прямо в браузері
files = st.sidebar.file_uploader("Завантажте CSV файли", accept_multiple_files=True)

data = {}
if files:
    for file in files:
        data[file.name] = pd.read_csv(file)
    
    # Якщо завантажено games-list.csv
    if "games-list.csv" in data:
        df = data["games-list.csv"]
        df['revenue'] = df['copiesSold'] * df['price']
        
        st.subheader("🚀 Топ ігор за виторгом")
        top_n = st.slider("Кількість ігор", 5, 30, 10)
        fig = px.bar(df.sort_values('revenue', ascending=False).head(top_n), 
                     x='revenue', y='name', orientation='h', color='revenue')
        st.plotly_chart(fig, use_container_width=True)

    # Якщо завантажено genres.csv
    if "genres.csv" in data:
        st.subheader("📂 Аналітика жанрів")
        df_g = data["genres.csv"]
        fig2 = px.scatter(df_g, x="averagePrice", y="averageRevenue", 
                          size="numberOfGames", hover_name="label")
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("👋 Привіт! Закинь сюди свої CSV файли з Gamalytic у бічне меню ліворуч.")
