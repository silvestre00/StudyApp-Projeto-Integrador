import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import select, insert
from utils.storage import session, questions, answers, quiz_results, disciplines

def run():
    st.title("📝 Quiz / Simulados")

    # Carregar questões do banco
    query = select(questions)
    result = session.execute(query).fetchall()

    if not result:
        st.info("Nenhuma questão cadastrada ainda.")
        return

    score = 0
    total = len(result)
    user_answers = []

    # Exibir questões dinamicamente
    for q in result:
        st.subheader(q.text)

        opts = session.execute(
            select(answers).where(answers.c.question_id == q.id)
        ).fetchall()

        if not opts:
            st.warning("⚠️ Nenhuma alternativa cadastrada para esta questão.")
            continue

        option_texts = [opt.text for opt in opts]

        user_answer = st.radio(
            "Escolha uma resposta:",
            options=option_texts,
            key=f"q_{q.id}"
        )

        user_answers.append((q.id, user_answer))

    # Botão final para enviar o quiz
    if st.button("Finalizar Quiz"):
        for q_id, user_answer in user_answers:
            correct = session.execute(
                select(answers).where(
                    (answers.c.question_id == q_id) & (answers.c.is_correct == True)
                )
            ).fetchone()

            if correct and user_answer == correct.text:
                score += 1

        # Salvar resultado no banco
        stmt = insert(quiz_results).values(
            score=score,
            total_questions = total
        )
        session.execute(stmt)
        session.commit()

        # Mostrar resultado
        st.success(f"🎉 Quiz finalizado! Sua pontuação: {score}/{total}")

        # ======================
        # 📊 Estatísticas
        # ======================

        results = session.execute(select(quiz_results)).fetchall()
        if results:
            df = pd.DataFrame(results, columns=["id", "discipline_id", "score", "total", "created_at"])
            st.subheader("📊 Histórico de Tentativas")
            st.dataframe(df[["score", "total", "created_at"]])

            # Gráfico de evolução da pontuação
            fig_line = px.line(
                df,
                x="created_at",
                y="score",
                title="📈 Evolução das Pontuações",
                markers=True
            )
            st.plotly_chart(fig_line)

            # Acertos por disciplina (se as questões tiverem disciplina_id)
            q_with_disc = session.execute(select(questions)).fetchall()
            if q_with_disc:
                stats = []
                for q in q_with_disc:
                    correct = session.execute(
                        select(answers).where(
                            (answers.c.question_id == q.id) & (answers.c.is_correct == True)
                        )
                    ).fetchone()
                    if correct:
                        stats.append({
                            "discipline_id": q.discipline_id,
                            "question": q.text
                        })

                if stats:
                    stats_df = pd.DataFrame(stats)
                    # Juntar disciplinas
                    disc = session.execute(select(disciplines)).fetchall()
                    disc_df = pd.DataFrame(disc, columns=["id", "name", "minutes"])
                    merged = stats_df.merge(disc_df, left_on="discipline_id", right_on="id")

                    fig_bar = px.bar(
                        merged,
                        x="name",
                        title="📊 Questões por Disciplina",
                        labels={"name": "Disciplina", "count": "Qtd. Questões"}
                    )
                    st.plotly_chart(fig_bar)

if __name__ == "__main__":
    run()
