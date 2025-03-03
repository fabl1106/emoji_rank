from sqlalchemy import Column, Integer, String, ForeignKey

from conf import database


class User(database.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=True) # display name
    slack_id = Column(String(50), nullable=False) # 슬랙 아이디
    my_reaction = Column(Integer, nullable=False, default=5) # 사용할 수 있는 리액션(이모지) 개수
    avatar_url = Column(String(100), nullable=True)  # 프로필 이미지 url


class Reaction(database.Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False) # 년
    month = Column(Integer, nullable=False) # 월
    to_user = Column(Integer, ForeignKey("users.id")) # 리액션을 받은 유저
    from_user = Column(Integer, ForeignKey("users.id")) # 리액션을 보낸 유저
    type = Column(String(50), nullable=True) # 리액션 타입 (이모지 종류)
    count = Column(Integer, default=0) # 받은 개수
