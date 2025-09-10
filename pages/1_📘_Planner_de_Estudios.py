import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import insert, select
from utils.storage import session, disciplines
from utils.helpers import hours_to_minutes, minutes_to_hours

def load_data():
    query = select(disciplines)
    result = session.execute(query).fetchall()
    df = pd.DataFrame(result, columns=["id", "name", "minutes"])
    df.rename(columns={"name": "Disciplina", "minutes": "Minutos"}, inplace=True)
    return df

def save_discipline(name, minutes):
    stmt = insert(disciplines).values(name=name, minutes=minutes)
    session.execute(stmt)
    session.commit()

st.title("📘 Planner de Estudos")

with st.form("form_disciplines"):
    discipline_name = st.text_input("Nome da disciplina")

    col1, col2 = st.columns(2)
    hours = col1.number_input("Horas", min_value=0, max_value=40, step=1)
    minutes = col2.number_input("Minutos", min_value=0, max_value=59, step=5)

    submit = st.form_submit_button("Adicionar")

    if submit:
        if discipline_name and (hours > 0 or minutes > 0):
            total_minutes = hours_to_minutes(int(hours), int(minutes))
            save_discipline(discipline_name, total_minutes)
            st.success(f"✅ {discipline_name} adicionada com {hours}:{minutes:02d}h semanais!")
        else:
            st.error("⚠️ Preencha os campos corretamente.")

df = load_data()

st.subheader("📋 Disciplinas Cadastradas")
if df.empty:
    st.info("Nenhuma disciplina cadastrada ainda.")
else:
    df["Tempo de Estudo"] = df["Minutos"].apply(minutes_to_hours)
    st.dataframe(df[["Disciplina", "Tempo de Estudo"]])

    st.subheader("📊 Distribuição de Horas")
    fig_pizza = px.pie(df, names="Disciplina", values="Minutos", title="Distribuição por Disciplina")
    st.plotly_chart(fig_pizza)

    fig_barras = px.bar(df, x="Disciplina", y="Minutos", text="Minutos", title="Tempo semanal por Disciplina")
    st.plotly_chart(fig_barras)
