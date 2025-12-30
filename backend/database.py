
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url="postgresql://postgres:Lakshayaa@localhost:5432/fastapiDEMO"
engine=create_engine(db_url)
SessionLocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)
