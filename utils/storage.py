from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///data/estudos.db"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

disciplines = Table(
    "disciplines", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("minutes", Integer, nullable=False)
)

metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()