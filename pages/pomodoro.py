import streamlit as st
import time
from datetime import datetime
from sqlalchemy import insert, select
from utils.storage import session, disciplines, pomodoro_sessions


# Função para carregar disciplinas do banco
def get_disciplines():
    query = select(disciplines.c.id, disciplines.c.name)
    return session.execute(query).fetchall()


# Função para salvar sessão no banco
def save_pomodoro_session(discipline_id, focus_minutes, break_minutes, start_time, end_time):
    stmt = insert(pomodoro_sessions).values(
        discipline_id=discipline_id,
        focus_minutes=focus_minutes,
        break_minutes=break_minutes,
        start_time=start_time,
        end_time=end_time
    )
    session.execute(stmt)
    session.commit()


def run():
    st.title("⏱️ Modo Foco - Pomodoro")

    # Seleção da disciplina
    discipline_list = get_disciplines()
    if not discipline_list:
        st.warning("⚠️ Nenhuma disciplina cadastrada. Cadastre no Planner antes de usar o Pomodoro.")
        return

    discipline_names = [d.name for d in discipline_list]
    selected_discipline = st.selectbox("Selecione a disciplina", discipline_names)

    # Recupera o ID da disciplina escolhida
    discipline_id = None
    for d in discipline_list:
        if d.name == selected_discipline:
            discipline_id = d.id
            break

    col1, col2 = st.columns(2)
    focus_time = col1.number_input("Tempo de foco (minutos)", min_value=1, max_value=120, value=25, step=1)
    break_time = col2.number_input("Tempo de pausa (minutos)", min_value=1, max_value=30, value=5, step=1)

    if st.button("Iniciar Pomodoro"):
        st.session_state["running"] = True
        st.session_state["focus_time"] = focus_time
        st.session_state["break_time"] = break_time
        st.session_state["discipline_id"] = discipline_id
        st.session_state["start_time"] = datetime.utcnow()

    if "running" in st.session_state and st.session_state["running"]:
        st.subheader(f"📘 Disciplina: {selected_discipline}")

        total_seconds = st.session_state["focus_time"] * 60
        with st.empty():
            for remaining in range(total_seconds, 0, -1):
                mins, secs = divmod(remaining, 60)
                st.metric("⏳ Tempo restante (foco)", f"{mins:02}:{secs:02}")
                time.sleep(1)

        st.success("✅ Tempo de foco concluído! Agora, faça uma pausa.")

        # Salva a sessão no banco
        save_pomodoro_session(
            st.session_state["discipline_id"],
            st.session_state["focus_time"],
            st.session_state["break_time"],
            st.session_state["start_time"],
            datetime.utcnow()
        )

        st.session_state["running"] = False

if __name__ == "__main__":
    run()
