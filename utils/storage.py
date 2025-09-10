from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

os.makedirs("data", exist_ok=True)

DATABASE_URL = "sqlite:///data/estudos.db"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

disciplines = Table(
    "disciplines", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("minutes", Integer, nullable=False)
)

questions = Table(
    "questions", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("discipline_id", Integer, ForeignKey("disciplines.id")),
    Column("text", String, nullable=False)
)

answers = Table(
    "answers", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("question_id", Integer, ForeignKey("questions.id")),
    Column("text", String, nullable=False),
    Column("created_at", DateTime, default=datetime.utcnow)
)

quiz_results = Table(
    "quiz_results", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("discipline_id", Integer, ForeignKey("disciplines.id")),
    Column("score", Integer, nullable=False),
    Column("total_questions", Integer, nullable=False),
    Column("created_at", DateTime, default=datetime.utcnow)
)

metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()