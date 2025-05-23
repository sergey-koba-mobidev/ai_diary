import os
from sqlalchemy import Column, Integer, String, DateTime, Table, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


def postgres_session():
    db = create_engine(os.environ.get("POSTGRES_URL"))
    session_maker = sessionmaker(bind=db)
    return session_maker()


# Association table
diary_records_tags_association = Table(
    "diary_records_tags_association",
    Base.metadata,
    Column(
        "diary_record_id", Integer, ForeignKey("diary_records.id"), primary_key=True
    ),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class DiaryRecord(Base):
    __tablename__ = "diary_records"

    id = Column(Integer, primary_key=True)
    happened_at = Column(DateTime(timezone=True), nullable=False)
    body = Column(String, nullable=False)
    llm_response = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Many-to-many relationships
    tags = relationship(
        "Tag", secondary=diary_records_tags_association, back_populates="diary_records"
    )


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Many-to-many relationships
    diary_records = relationship(
        "DiaryRecord",
        secondary=diary_records_tags_association,
        back_populates="tags",
    )
