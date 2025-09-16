import streamlit as st
import pandas as pd
from sqlalchemy import insert, select
from utils.storage import session, flashcards

def load_flashcards():
    query = select(flashcards)
    result = session.execute(query).fetchall()
    df = pd.DataFrame(result, columns=["id", "front", "back", "created_at"])
    return df

def save_flashcard(front, back):
    stmt = insert(flashcards).values(front=front, back=back)
    session.execute(stmt)
    session.commit()

def run():
    st.title("🃏 Flashcards")

    # Formulário
    with st.form("flashcard_form"):
        col1, col2 = st.columns(2)
        front = col1.text_input("Frente (pergunta ou palavra-chave)")
        back = col2.text_input("Verso (resposta ou explicação)")
        submit = st.form_submit_button("Adicionar Flashcard")

        if submit:
            if not front or not back:
                st.warning("⚠️ Preencha os dois campos para salvar o flashcard.")
            else:
                save_flashcard(front, back)
                st.success("✅ Flashcard adicionado com sucesso!")

    # Listagem de Flashcards
    st.subheader("📋 Meus Flashcards")
    df = load_flashcards()

    if df.empty:
        st.info("Nenhum flashcard cadastrado ainda.")
    else:
        for _, row in df.iterrows():
            with st.expander(f"🔹 {row['front']}"):
                st.write(row["back"])
