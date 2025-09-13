from sqlalchemy import (
    create_engine, Colum, Integer, String, Table, Metada, Boolean, ForeignKey, DateTime, select
)
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from utils.seed_data import seed_questions


# Garantir que a pasta do banco existe
os.makedirs("data", exist_ok=True)

#Caminho para o banco SQLite
DATABASE_URL = "sqlite:///data/estudos.db"

# Criação do engine e metada
engine = create_engine(DATABASE_URL, echo=False, future=True)
metadata = MetaData()

#---------Tabelas-----------
# Disciplinas
disciplines = Table(
    "disciplines", metadata,
   "disciplines", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False, unique=True),
    Column("minutes", Integer, nullable=False, default=0)
)
# Perguntas do quiz
questions = Table(
    "questions", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("discipline_id", Integer, ForeignKey("disciplines.id", ondelete="CASCADE")),
    Column("text", String, nullable=False)
)

# Respostas das perguntas 
answers = Table(
    "answers", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("question_id", Integer, ForeignKey("questions.id", ondelete="CASCADE")),
    Column("text", String, nullable=False),
    Column("is_correct", Boolean, default=False),  # importante para o quiz!
    Column("created_at", DateTime, default=datetime.utcnow)
)

# Resultados dos quizzes
quiz_results = Table(
    "quiz_results", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("discipline_id", Integer, ForeignKey("disciplines.id", ondelete="SET NULL")),
    Column("score", Integer, nullable=False),
    Column("total_questions", Integer, nullable=False),
    Column("created_at", DateTime, default=datetime.utcnow)
)

# Cria todas as tabelas (Caso não existam)
metadata.create_all(engine)

#Sessão de conexão
Session = sessionmaker(bind=engine, future=True)
session = Session()

# Popular o banco com exemplo
# Verifica se já existem perguntas
if session.execute(select(questions)).first() is None:
    seed_questions()