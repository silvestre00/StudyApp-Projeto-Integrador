import streamlit as st

from modules import planner

st.sidebar.title("📚 Aplicativo de Estudos")
menu = st.sidebar.radio("Escolha um módulo:", ["Planner de Estudos", ])

if menu == "Planner de Estudos":
    planner.run()