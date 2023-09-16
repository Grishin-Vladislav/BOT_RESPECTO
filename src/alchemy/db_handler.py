from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from alchemy.models import *
from config import *


class DbHandler:
    def __init__(self, DSN):
        self.__engine = sqlalchemy.create_engine(DSN)

        if not database_exists(self.__engine.url):
            create_database(self.__engine.url)
            self.__create_tables(self.__engine)
        else:
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
        conv = Conversation(date=datetime.now(),
                            chat_id=chat_id,
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

    def get_quota(self, chat_id: int):
        quota = self.__s.query(Quota).filter(Quota.chat_id == chat_id).first()
        return quota

    def get_all_chats(self):
        all_chats_objects = self.__s.query(Quota).all()
        all_chats = [chat.chat_id for chat in all_chats_objects]
        return all_chats

    def change_quota(self, chat_id: int, amount: int):
        quota = self.get_quota(chat_id)
        quota.remaining = amount
        self.__s.add(quota)
        self.commit()

    def create_quoted_chat(self, chat_id: int, quota: int):
        quota = Quota(chat_id=chat_id, remaining=quota)
        self.__s.add(quota)
        self.commit()

    def reset_quota_for_all(self):
        all_chats = self.__s.query(Quota).all()

        for chat in all_chats:
            if PREMIUM.get(str(chat.chat_id)):
                chat.remaining = PREMIUM[str(chat.chat_id)]
            else:
                chat.remaining = REGULAR_DAILY_QUOTA
            self.__s.add(chat)

        self.commit()

    def remove_inactive_chats(self, kicked):
        query = self.__s.query(Quota).filter(Quota.chat_id.in_(kicked))
        inactive = query.all()

        for quota in inactive:
            self.__s.delete(quota)

        self.commit()

    def write_to_event_register(self, user_id, username, date):
        record = EventRegister(
            user_id=user_id,
            user_name=username,
            date=date
        )
        self.__s.add(record)
        self.commit()

    def is_already_registered(self, user_id):
        q = self.__s.query(EventRegister).filter(
            EventRegister.user_id == user_id).first()

        if q:
            return True
        return False

    def get_all_event_registered(self):
        all_chats_objects = self.__s.query(EventRegister).all()
        all_chats = [chat.user_id for chat in all_chats_objects]
        return all_chats

    def commit(self):
        try:
            self.__s.commit()
        except:
            self.__s.rollback()

    @staticmethod
    def __create_tables(engine) -> None:
        Base.metadata.create_all(engine)
