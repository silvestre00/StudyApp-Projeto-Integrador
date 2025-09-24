# pages/gestor_entregas.py

import streamlit as st
import datetime
from utils.storage import Entrega, add_entrega, get_entregas, get_alertas
from utils.storage import sessionmaker, create_engine, Base
from streamlit_calendar import calendar

# --- Configuração do banco ---
engine = create_engine("sqlite:///data/estudos.db")
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

st.title("📚 Gestor de Provas e Trabalhos")

# --- RF18: Alertas ---
alertas = get_alertas(session, dias=7)
if alertas:
    st.warning("⚠️ Você tem entregas próximas!")
    for entrega in alertas:
        dias_restantes = (entrega.data - datetime.date.today()).days
        st.write(f"📌 {entrega.nome} — {entrega.data.strftime('%d/%m/%Y')} (faltam {dias_restantes} dias)")

st.divider()

# --- RF16: Cadastro ---
st.subheader("Cadastrar nova entrega")
with st.form("cadastro_entrega"):
    nome = st.text_input("Nome da prova/trabalho")
    data = st.date_input("Data da entrega", min_value=datetime.date.today())
    submitted = st.form_submit_button("Cadastrar")
    if submitted and nome:
        add_entrega(session, nome, data)
        st.success("Entrega cadastrada com sucesso!")
        st.rerun()

st.divider()

# --- RF17 + RF19: Listagem ordenada ---
st.subheader("📋 Lista de entregas")
entregas = get_entregas(session)
if entregas:
    for entrega in entregas:
        st.write(f"📌 {entrega.nome} — {entrega.data.strftime('%d/%m/%Y')}")
else:
    st.info("Nenhuma entrega cadastrada ainda.")

st.divider()

# --- RF17: Calendário Interativo ---
st.subheader("📅 Calendário de entregas")

if entregas:
    eventos = []
    for entrega in entregas:
        eventos.append({
            "title": entrega.nome,
            "start": entrega.data.strftime("%Y-%m-%d"),
            "end": entrega.data.strftime("%Y-%m-%d"),
        })

    calendar_options = {
        "editable": False,
        "selectable": False,
        "initialView": "dayGridMonth",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay",
        },
    }

    calendar(events=eventos, options=calendar_options)
else:
    st.info("Nenhuma entrega cadastrada para exibir no calendário.")
