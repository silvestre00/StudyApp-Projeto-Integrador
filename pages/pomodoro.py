import streamlit as st
import time
from datetime import datetime
from sqlalchemy import insert, update, select
from utils.storage import session, disciplines, focus_sessions

def run():
    st.title("⏳ Modo Foco (Pomodoro)")

    # Carregar disciplinas cadastradas
    query = select(disciplines)
    result = session.execute(query).fetchall()
    discipline_options = ["-- Nenhuma --"] + [row.name for row in result]

    # Formulário para configurar sessão
    with st.form("focus_form"):
        selected_discipline = st.selectbox("Selecione uma disciplina (opcional)", discipline_options)
        duration = st.number_input("Duração (minutos)", min_value=1, max_value=120, value=25, step=5)
        start_btn = st.form_submit_button("Iniciar sessão")

    if start_btn:
        # Pegar discipline_id (ou None)
        discipline_id = None
        if selected_discipline != "-- Nenhuma --":
            disc_row = next((row for row in result if row.name == selected_discipline), None)
            discipline_id = disc_row.id if disc_row else None

        # Criar registro no banco
        stmt = insert(focus_sessions).values(
            discipline_id=discipline_id,
            duration_minutes=duration,
            started_at=datetime.utcnow(),
            status="running"
        )
        result_insert = session.execute(stmt)
        session.commit()

        session_id = result_insert.inserted_primary_key[0]

        st.session_state["focus_session_id"] = session_id
        st.session_state["focus_end_time"] = time.time() + duration * 60
        st.session_state["focus_running"] = True
        st.rerun()

    # Controle do timer
    if st.session_state.get("focus_running", False):
        session_id = st.session_state["focus_session_id"]
        end_time = st.session_state["focus_end_time"]

        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("⏱️ Sessão em andamento")
        with col2:
            if st.button("Encerrar sessão"):
                stmt = (
                    update(focus_sessions)
                    .where(focus_sessions.c.id == session_id)
                    .values(finished_at=datetime.utcnow(), status="interrupted")
                )
                session.execute(stmt)
                session.commit()
                st.success("⚠️ Sessão interrompida.")
                st.session_state["focus_running"] = False
                st.rerun()

        # Mostrar timer
        remaining = int(end_time - time.time())
        if remaining > 0:
            mins, secs = divmod(remaining, 60)
            st.markdown(f"## ⌛ {mins:02d}:{secs:02d}")
            time.sleep(1)
            st.rerun()
        else:
            # Sessão concluída
            stmt = (
                update(focus_sessions)
                .where(focus_sessions.c.id == session_id)
                .values(finished_at=datetime.utcnow(), status="completed")
            )
            session.execute(stmt)
            session.commit()
            st.success("✅ Sessão concluída com sucesso!")
            st.session_state["focus_running"] = False

if __name__ == "__main__":
    run()
