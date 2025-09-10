import streamlit as st
import pandas as pd
from sqlalchemy import insert, select
from utils.storage import session, disciplines, questions, answers

def add_question(discipline_id, text, options, correct_index):
    stmt = insert(questions).values(discipline_id=discipline_id, text=text)
    result = session.execute(stmt)
    question_id = result.inserted_primary_key[0]

    for i, option in enumerate(options):
        stmt = insert(answers).values(question_id=question_id, text=option, is_correct=(i==correct_index))
        session.execute(stmt)
    
    session.commit()

st.title("📝 Quiz / Simulados")

st.subheader("Adicionar Nova Pergunta")

query = select(disciplines)
df_disc = pd.DataFrame(session.execute(query).fetchall(), columns=["id", "name", "minutes"])

if df_disc.empty:
    st.warning("⚠️ Cadastre uma disciplina no Planner antes de criar perguntas.")
else:
    discipline_name = st.selectbox("Selecione a disciplina", df_disc["name"])
    discipline_id = df_disc.loc[df_disc["name"] == discipline_name, "id"].values[0]

    question_text = st.text_area("Enunciado da pergunta")

    options = []
    for i in range(4):
        options.append(st.text_input(f"Alternativa {i+1}", key=f"opt{i}"))
    
    correct_index = st.radio("Qual é a alternativa correta?", [0, 1, 2, 3], format_func=lambda x: f"Alternativa {x+1}")

    if st.button("Salvar Pergunta"):
        if question_text and all(options):
            add_question(discipline_id, question_text, options, correct_index)
            st.success("✅ Pergunta adicionada com sucesso!")
        else: st.error("⚠️ Preencha todos os campos.")