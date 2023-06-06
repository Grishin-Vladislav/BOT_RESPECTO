import sqlalchemy
from sqlalchemy.orm import sessionmaker
from alchemy.models import *
from config import *
from datetime import datetime
from sqlalchemy_utils import database_exists, create_database


class DbHandler:
    def __init__(self, DSN):
        self.__engine = sqlalchemy.create_engine(DSN)
        if not database_exists(self.__engine.url):
            create_database(self.__engine.url)
            self.__create_tables(self.__engine)

        self.__Session = sessionmaker(bind=self.__engine)
        self.__s = None

    def __enter__(self):
        self.__s = self.__Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__s:
            self.__s.close()

    def record_conversation(self, chat_id):
        conv = Conversation(date=datetime.now(), chat_id=chat_id,
                            temperature=REPLY_TEMP,
                            presence_penalty=REPLY_PRES_PENALTY,
                            frequency_penalty=REPLY_FREQ_PENALTY,
                            max_tokens=REPLY_MAX_TOKENS,
                            model=REPLY_MODEL)
        self.__s.add(conv)
        self.commit()
        return conv.id

    def record_character(self, conversation_id, name, prompt):
        char = Character(conversation_id=conversation_id,
                         name=name,
                         temperature=GEN_TEMP,
                         presence_penalty=GEN_PRES_PENALTY,
                         frequency_penalty=GEN_FREQ_PENALTY,
                         max_tokens=GEN_MAX_TOKENS,
                         model=GEN_MODEL,
                         prompt=prompt)
        self.__s.add(char)
        self.commit()
        return char.id

    def record_message(self, character_id, conversation_id, text,
                       user: bool):
        mes = Message(character_id=character_id,
                      conversation_id=conversation_id,
                      user=user, text=text)
        self.__s.add(mes)
        self.commit()

    def mark_conversation_win(self, state: bool, conversation_id):
        conv = self.__s.query(Conversation).filter(
            Conversation.id == conversation_id).update({'win': state})
        self.commit()

    def commit(self):
        try:
            self.__s.commit()
        except:
            self.__s.rollback()

    @staticmethod
    def __create_tables(engine) -> None:
        Base.metadata.create_all(engine)
