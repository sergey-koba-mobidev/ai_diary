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
    "diary_records_tags_association",  # diary_records table has many tags through diary_records_tags_association table, which has diary_record_id foreign key and tag_id foreign key
    Base.metadata,
    Column(
        "diary_record_id", Integer, ForeignKey("diary_records.id"), primary_key=True
    ),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class DiaryRecord(Base):
    __tablename__ = "diary_records"  # diary_records - This is a table, which stores diary records of the author, who calls himself Сергей

    id = Column(Integer, primary_key=True)  # id - primary key for diary_records table
    happened_at = Column(
        DateTime(timezone=True), nullable=False
    )  # happened_at - this is the date when this diary record happened
    body = Column(
        String, nullable=False
    )  # body - the text of the diary record with informaiton what happened this day with Сергей
    mood = Column(String)  # mood - Description of the authoor's mood. Can be null.
    mood_mark = Column(
        Integer
    )  # mood_mark - Author's Mood assessment value, from 0 to 10, 0 - very bad, 10 - excellent. Can be null.
    health = Column(
        String
    )  # health - Description of the authoor's health. Can be null.
    health_mark = Column(
        Integer
    )  # health_mark - Author's health assessment value, from 0 to 10, 0 - very bad, 10 - excellent. Can be null.
    health_reason = Column(
        String
    )  # health_reason - explanation, why health_mark has such a value. Can be null.
    weather = Column(
        String
    )  # weather - description of the weather this day. Can be null.
    illness = Column(
        String
    )  # illness - description of the illnesses experienced by author this day. Can be null.
    summary = Column(String)  # summary - short description of the day. Can be null.
    llm_response = Column(
        JSONB
    )  # llm_reponse - field with json from LLM analyzing this diary record
    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )  # created_at - datetime when this record was created
    updated_at = Column(
        DateTime(timezone=True), onupdate=func.now()
    )  # updated_at - datetime when this record was updated

    # Many-to-many relationships
    tags = relationship(
        "Tag", secondary=diary_records_tags_association, back_populates="diary_records"
    )  # diary_records table has many tags through diary_records_tags_association table, which has diary_record_id foreign key and tag_id foreign key
    persons = relationship(
        "Person",
        secondary="actions",
        back_populates="diary_records",
    )  # diary_records table has many persons through actions table, which has diary_record_id foreign key and person_id foreign key


class Tag(Base):
    __tablename__ = "tags"  # tags table contains keywords describing diary record

    id = Column(Integer, primary_key=True)  # id - primary key of tags table
    title = Column(String, nullable=False)  # title - name of the tag
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Many-to-many relationships
    # tags table has many diary_records through diary_records_tags_association table, which has diary_record_id foreign key and tag_id foreign key
    diary_records = relationship(
        "DiaryRecord",
        secondary=diary_records_tags_association,
        back_populates="tags",
    )


class Action(Base):
    __tablename__ = "actions"  # actions is an association table between diary_records and persons tables containing information who did what on particular diary_record day

    id = Column(Integer, primary_key=True)  # id - primary key of the actions table
    name = Column(
        String, nullable=False
    )  # name - name of the action, what a person did. Exmaple: had a walk
    diary_record_id = Column(
        Integer, ForeignKey("diary_records.id")
    )  # diary_record_id - foreign key to diary_records table
    person_id = Column(
        Integer, ForeignKey("persons.id")
    )  # person_id - foreign key to persons table
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    diary_record = relationship("DiaryRecord", backref="actions", viewonly=True)
    person = relationship("Person", backref="actions", viewonly=True)


class Person(Base):
    __tablename__ = "persons"  # persons table contains a list of persons that are mentioned in diary_records and take some actions on that day

    id = Column(Integer, primary_key=True)  # id - primary key of persons table
    name = Column(String, nullable=False)  # name - name of the person

    # Many-to-many relationships
    # persons table has many diary_records through actions table, which has diary_record_id foreign key and person_id foreign key
    diary_records = relationship(
        "DiaryRecord",
        secondary="actions",
        back_populates="persons",
    )


class Sleep(Base):
    __tablename__ = (
        "sleeps"  # sleeps table contains information about diary author Сергей sleep
    )

    id = Column(Integer, primary_key=True)  # id - primary key of sleeps table
    deep_sleep_time = Column(
        Integer
    )  # deep_sleep_time - amount of minutes author had deep sleep this day (happened_at)
    shallow_sleep_time = Column(
        Integer
    )  # deep_sleep_time - amount of minutes author had shallow sleep this day (happened_at)
    rem_time = Column(
        Integer
    )  # deep_sleep_time - amount of minutes author had REM sleep this day (happened_at)
    total_sleep_time = Column(
        Integer, nullable=False
    )  # total_sleep_time = deep_sleep_time + shallow_sleep_time + rem_time. Total amount of minutes author had sleep this day (happened_at)
    wake_time = Column(Integer)
    start_at = Column(
        DateTime(timezone=True)
    )  # start_at - datetime when author started to sleep this day (happened_at)
    stop_at = Column(
        DateTime(timezone=True)
    )  # stop_at - datetime when author stopped sleeping this day (happened_at)
    naps = Column(Integer)  # naps - number of naps author had this day (happened_at)
    happened_at = Column(
        DateTime(timezone=True), nullable=False
    )  # happened_at - datetime to which this sleep info belongs. Can have the same date as happened_at in diary_records table
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
