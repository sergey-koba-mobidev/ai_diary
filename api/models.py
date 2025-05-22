import os
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def postgres_session():
    db = create_engine(os.environ.get("POSTGRES_URL"))
    session_maker = sessionmaker(bind=db)
    return session_maker()


class DiaryRecord(Base):
    __tablename__ = "diary_records"

    id = Column(Integer, primary_key=True)
    happened_at = Column(DateTime(timezone=True), nullable=False)
    body = Column(String, nullable=False)
    llm_response = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
