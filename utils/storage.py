from sqlalchemy import (
    create_engine, Column, Integer, String, Table, MetaData, Boolean, ForeignKey, DateTime, Date, text, select
)
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, date, timedelta
import os

# Garantir que a pasta do banco existe
os.makedirs("data", exist_ok=True)

# Caminho para o banco SQLite
DATABASE_URL = "sqlite:///data/estudos.db"

# Criação do engine e metadata
engine = create_engine(DATABASE_URL, echo=False, future=True)
metadata = MetaData()

# --------- Tabelas (modo Table) ----------
# Disciplinas
disciplines = Table(
    "disciplines", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False, unique=True),
    Column("minutes", Integer, nullable=False, server_default=text("0"))
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
    Column("is_correct", Boolean, default=False),
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

# Flashcards
flashcards = Table(
    "flashcards", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("front", String, nullable=False),
    Column("back", String, nullable=False),
    Column("created_at", DateTime, default=datetime.utcnow)
)

# Focus (Pomodoro)
pomodoro_sessions = Table(
    "pomodoro_sessions", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("discipline_id", Integer, ForeignKey("disciplines.id", ondelete="SET NULL"), nullable=True),
    Column("focus_minutes", Integer, nullable=False),
    Column("break_minutes", Integer, nullable=False),
    Column("start_time", DateTime, default=datetime.utcnow),
    Column("end_time", DateTime, nullable=True),
    Column("status", String, default="completed"),  # completed | interrupted
)

# --------- ORM Base (para entregas) ----------
Base = declarative_base()

class Entrega(Base):
    __tablename__ = "entregas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    data = Column(Date, nullable=False)

# --------- Funções auxiliares ----------
def add_entrega(session, nome, data):
    """
    Adiciona uma nova entrega (prova/trabalho) ao banco de dados.
    """
    nova = Entrega(nome=nome, data=data)
    session.add(nova)
    session.commit()

def get_entregas(session):
    """
    Retorna todas as entregas, ordenadas pela data.
    """
    return session.query(Entrega).order_by(Entrega.data.asc()).all()

def get_alertas(session, dias=7):
    """
    Retorna entregas que estão a até 'dias' da data atual.
    """
    hoje = date.today()
    limite = hoje + timedelta(days=dias)
    return (
        session.query(Entrega)
        .filter(Entrega.data >= hoje, Entrega.data <= limite)
        .order_by(Entrega.data.asc())
        .all()
    )

# --------- Criação das tabelas ----------
metadata.create_all(engine)       # cria tabelas "Table"
Base.metadata.create_all(engine)  # cria tabelas do ORM

# Sessão de conexão
Session = sessionmaker(bind=engine, future=True)
session = Session()

# Popular o banco com dados de exemplo (seed)
def run_seed_if_needed():
    from utils.seed_data import seed_questions
    if session.execute(select(questions)).first() is None:
        seed_questions()

run_seed_if_needed()
