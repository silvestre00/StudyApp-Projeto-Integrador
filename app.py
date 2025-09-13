import streamlit as st

def main():
    planner_page = st.Page(
        "pages/planner.py", url_path="/planner", title="PLanner de Estudos", icon="📘"
    )
    quiz_page = st.Page(
        "pages/quiz.py", url_path="/quiz", title="Quiz / Simulados", icon="📝"
    )
    flashcards_page = st.Page(
        "pages/flashcards.py", url_path="/flashcards", title="Flashcards", icon="🃏"
    )
    summaries_page = st.Page(
        "pages/summaries.py", url_path="/summaries", title="Resumo Inteligente", icon="🧾"
    )
    tasks_page = st.Page(
        "pages/tasks.py", url_path="/tasks", title="Provas & Trabalhos", icon="📅"
    )
    stats_page = st.Page(
        "pages/stats.py", url_path= "/stats", title="Estatísticas", icon="📊"
    )
    pomodoro_page = st.Page(
        "pages/pomodoro.py", url_path="/pomodoro", title="Modo Foco", icon="⏱️"
    )

    pg = st.navigation(
        [
            planner_page,
            quiz_page,
            flashcards_page,
            summaries_page,
            tasks_page,
            stats_page,
            pomodoro_page,
        ]
    )
    
    st.set_page_config(
        page_title="📚 StudyApp - Projeto Integrador",
        page_icon="📚",
        layout="wide",
    )

    pg.run()

if __name__ == "__main__":
    main()