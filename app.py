import streamlit as st

st.set_page_config(
    page_title="StudyApp",
    page_icon="📚",
    layout="wide"
)
st.title("📚 Aplicativo de Estudos")
st.markdown("""
    Bem-vindo ao **StudyApp**!  
    Use o menu lateral para navegar entre os módulos:
    - 📘 Planner de Estudos  
    - 📝 Quiz / Simulados  
    - 🃏 Flashcards  
    - 📑 Resumo Inteligente  
    - 📅 Gestor de Provas e Trabalhos  
    - 📊 Estatísticas de Estudo  
    - ⏱️ Modo Foco (Pomodoro) 
""")