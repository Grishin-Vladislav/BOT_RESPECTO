from sqlalchemy import Column, BIGINT, ForeignKey, Text, VARCHAR, Float, \
    INTEGER, TIMESTAMP, BOOLEAN
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Character(Base):
    __tablename__ = 'character'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    conversation_id = Column(BIGINT, ForeignKey('conversation.id'))
    name = Column(Text)
    model = Column(VARCHAR(15))
    temperature = Column(Float)
    presence_penalty = Column(Float)
    frequency_penalty = Column(Float)
    max_tokens = Column(INTEGER)
    prompt = Column(Text)

    conversation = relationship('Conversation', back_populates='character')
    message = relationship('Message', back_populates='character')


class Conversation(Base):
    __tablename__ = 'conversation'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    date = Column(TIMESTAMP)
    win = Column(BOOLEAN)
    chat_id = Column(INTEGER)
    model = Column(VARCHAR(15))
    temperature = Column(Float)
    presence_penalty = Column(Float)
    frequency_penalty = Column(Float)
    max_tokens = Column(INTEGER)

    character = relationship('Character', back_populates='conversation')
    message = relationship('Message', back_populates='conversation')


class Message(Base):
    __tablename__ = 'message'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    character_id = Column(BIGINT, ForeignKey('character.id'), nullable=False)
    conversation_id = Column(BIGINT, ForeignKey('conversation.id'), nullable=False)
    user = Column(BOOLEAN, nullable=False)
    text = Column(Text)

    character = relationship('Character', back_populates='message')
    conversation = relationship('Conversation', back_populates='message')