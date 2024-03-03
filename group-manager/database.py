
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_guid = Column(String(32), unique=True, nullable=True)
    name = Column(String, unique=True, nullable=False)
    lock_links = Column(Boolean, default=False)
    lock_hyperlinks = Column(Boolean, default=False)
    lock_usernames = Column(Boolean, default=False)
    lock_hashtags = Column(Boolean, default=False)
    lock_english = Column(Boolean, default=False)
    lock_persian = Column(Boolean, default=False)
    lock_text = Column(Boolean, default=False)
    lock_badwords = Column(Boolean, default=False)
    lock_forward = Column(Boolean, default=False)
    lock_inline = Column(Boolean, default=False)
    lock_authentication = Column(Boolean, default=False)
    lock_emojis = Column(Boolean, default=False)
    lock_files = Column(Boolean, default=False)
    lock_photos = Column(Boolean, default=False)
    lock_videos = Column(Boolean, default=False)
    lock_audios = Column(Boolean, default=False)
    lock_gifs = Column(Boolean, default=False)
    lock_stickers = Column(Boolean, default=False)
    lock_location = Column(Boolean, default=False)
    lock_contact = Column(Boolean, default=False)
    lock_sticker_commands = Column(Boolean, default=False)
    lock_media_commands = Column(Boolean, default=False)
    lock_voice_commands = Column(Boolean, default=False)
    lock_command_mention = Column(Boolean, default=False)
    lock_reply_spoiler = Column(Boolean, default=False)
    lock_polls = Column(Boolean, default=False)
    lock_story = Column(Boolean, default=False)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_guid = Column(String(32), unique=True, nullable=True)
    username = Column(String, unique=True, nullable=True)

class GroupUser(Base):
    __tablename__ = 'group_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_guid = Column(String(32), ForeignKey('users.user_guid'))
    group_guid = Column(String(32), ForeignKey('groups.group_guid'))
    role = Column(String, nullable=False)

class GroupOwner(Base):
    __tablename__ = 'group_owners'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_guid = Column(String(32), ForeignKey('groups.group_guid'))
    user_guid = Column(String(32), ForeignKey('users.user_guid'))

class GroupAdmin(Base):
    __tablename__ = 'group_admins'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_guid = Column(String(32), ForeignKey('groups.group_guid'))
    user_guid = Column(String(32), ForeignKey('users.user_guid'))

class VIPMember(Base):
    __tablename__ = 'vip_members'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_guid = Column(String(32), ForeignKey('groups.group_guid'))
    user_guid = Column(String(32), ForeignKey('users.user_guid'))

class FilterWord(Base):
    __tablename__ = 'filter_words'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_guid = Column(String(32), ForeignKey('groups.group_guid'))
    word = Column(String, nullable=False)

class MutedUser(Base):
    __tablename__ = 'muted_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_guid = Column(String(32), ForeignKey('groups.group_guid'))
    user_guid = Column(String(32), ForeignKey('users.user_guid'))

class BannedUser(Base):
    __tablename__ = 'banned_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_guid = Column(String(32), ForeignKey('groups.group_guid'))
    user_guid = Column(String(32), ForeignKey('users.user_guid'))

class ExemptUser(Base):
    __tablename__ = 'exempt_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_guid = Column(String(32), ForeignKey('groups.group_guid'))
    user_guid = Column(String(32), ForeignKey('users.user_guid'))

class Warning(Base):
    __tablename__ = 'warnings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_guid = Column(String(32), ForeignKey('groups.group_guid'))
    user_guid = Column(String(32), ForeignKey('users.user_guid'))
    reason = Column(Text)

class UserAuthentication(Base):
    __tablename__ = 'user_authentications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_guid = Column(String(32), nullable=False)
    user_guid = Column(String(32), nullable=False)
    equation = Column(String, nullable=False)
    expected_result = Column(Integer, nullable=False)
    auth = Column(Boolean, default=False)

# ایجاد یک موتور و جلسه برای ارتباط با دیتابیس
engine = create_engine('sqlite:///robot.db', echo=False, pool_size=10, max_overflow=20)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)