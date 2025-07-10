import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta

filename = 'workouts.json'

def load():
    if not os.path.exists(filename):
        return []
    f = open(filename, 'r', encoding='utf-8')
    data = json.load(f)
    f.close()
    return data

def save(data):
    f = open(filename, 'w', encoding='utf-8')
    json.dump(data, f, indent=4, ensure_ascii=False)
    f.close()

if 'data' not in st.session_state:
    st.session_state.data = load()

st.title("Трекер тренировок")

with st.form("add_form"):
    date = st.date_input("Дата")
    act = st.text_input("Вид активности")
    dur = st.text_input("Длительность в минутах")
    kcal = st.text_input("Сожжено калорий")
    btn = st.form_submit_button("Добавить")

    if btn:
       try:
           d, k = float(dur), float(kcal)
           if d <= 0 or k <= 0:
               st.error("Длительность и калории должны быть больше нуля!")
           else:
               st.session_state.data.append({
                   "date": str(date),
                   "type": act,
                   "duration": d,
                   "calories": k
               })
               save(st.session_state.data)
               st.success("Тренировка добавлена!")
       except ValueError:
        st.error("Введите числа в поля длительности и калорий!")

st.subheader("Статистика за период")

if len(st.session_state.data) == 0:
    st.info("Нет записей")
else:
    df = pd.DataFrame(st.session_state.data)
    df['date'] = pd.to_datetime(df['date'])
    df['duration'] = df['duration'].astype(float)
    df['calories'] = df['calories'].astype(float)

    period = st.selectbox("Выберите период:", ["За неделю", "За месяц"])

    today = datetime.now()
    if period == "За неделю":
        start = today - timedelta(days=7)
    else:
        start = today - timedelta(days=30)

    filtered = df[df['date'] >= start]
    grouped = filtered.groupby(filtered['date'].dt.date).agg({
        'duration': 'sum',
        'calories': 'sum'
    }).reset_index()
    grouped['date'] = grouped['date'].astype(str)

    st.write(f"**Статистика {period.lower()}**")
    st.dataframe(grouped)