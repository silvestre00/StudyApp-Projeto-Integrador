import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import insert, select, update
from utils.storage import session, disciplines
from utils.helpers import hours_to_minutes, minutes_to_hours

def load_data():
    query = select(disciplines)
    result = session.execute(query).fetchall()
    df = pd.DataFrame(result, columns=["id", "name", "minutes"])
    df.rename(columns={"name": "Disciplina", "minutes": "Minutos"}, inplace=True)
    return df

def save_discipline(name, minutes):
    query = select(disciplines).where(disciplines.c.name == name)
    existing = session.execute(query).fetchone()

    if existing:
        current_minutes = existing.minutes
        stmt = (
            update(disciplines).where(disciplines.c.id == existing.id).values(minutes=current_minutes + minutes)
        )
        session.execute(stmt)
    else:
        stmt = insert(disciplines).values(name=name, minutes=minutes)
        session.execute(stmt)
    session.commit()

def run():
    st.title("📘 Planner de Estudos")

    df = load_data()
    discipline_options = df["Disciplina"].tolist() if not df.empty else []

    with st.form("form_disciplines"):
        col1, col2 = st.columns(2)

        selected_discipline = col1.selectbox(
            "Selecione uma disciplina", options=["-- Nova disciplina --"] + discipline_options,
        )

        new_discipline = col1.text_input("Ou cadastre uma nova disciplina")\
            if selected_discipline == "-- Nova disciplina --" else None
        
        hours = col2.number_input("Horas", min_value=0, max_value=40, step=1)
        minutes = col2.number_input("Minutos", min_value=0, max_value=59, step=5)

        submit = st.form_submit_button("Salvar")

        if submit:
            discipline_name = new_discipline if selected_discipline == "-- Nova disciplina --" else selected_discipline

            if not discipline_name:
                st.warning("⚠️ Você precisa informar ou selecionar uma disciplina.")
            elif hours == 0 and minutes == 0:
                st.warning("⚠️ Defina pelo menos alguns minutos para a disciplina.")
            else:
                total_minutes = hours_to_minutes(int(hours), int(minutes))
                save_discipline(discipline_name, total_minutes)
                st.success(f"✅ {discipline_name} atualizada com +{hours}:{minutes:02d}h semanais!")
                
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


run()