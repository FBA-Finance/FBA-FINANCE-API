# database.py
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

MONGODB_URL = "mongodb+srv://admin:admin@cluster0.yby5j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = AsyncIOMotorClient(MONGODB_URL)
db = client.fba_finance

def get_db():
    return db



""" from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URL = 'sqlite:///./fbaf.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() """