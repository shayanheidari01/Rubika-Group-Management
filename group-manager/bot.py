from rubpy import Client, handlers, filters
from rubpy.types import Updates
from database import Session, User, Group
from new_group import AddGroup
from lock_option import SetLock
from get_status import GetStatus
from is_ads import IsAds

bot = Client('bot')
session = Session()

def is_event(update: Updates, result):
    return update.is_group and update.message.type == 'Event'

def is_hyperlink(update: Updates, result):
    if update.is_group and update.metadata:
        for part in update.metadata.meta_data_parts:
            if part.type == 'Link':
                return True

def is_mention_text(update: Updates, result):
    if update.is_group and update.metadata:
        for part in update.metadata.meta_data_parts:
            if part.type == 'MentionText':
                return True

def handle_hyperlinks(update: Updates):
    group = session.query(Group).filter_by(group_guid=update.object_guid).first()
    if group and group.lock_hyperlinks is True:
        update.reply('هایپرلینک است و حذف میشود.')
        return update.delete_messages()

def handle_mention_text(update: Updates):
    group = session.query(Group).filter_by(group_guid=update.object_guid).first()
    if group and group.lock_command_mention is True:
        update.reply('منشن است و حذف میشود.')
        return update.delete_messages()

def handle_events(update: Updates):
    group = session.query(Group).filter_by(group_guid=update.object_guid).first()
    if group:
        event_data = update.event_data
        author_guid = event_data.peer_objects[0].object_guid if event_data.peer_objects else event_data.object_guid
        get_author = update.get_author(author_guid)
        print(event_data.type)
        if event_data.type == 'LeaveGroup':
            update.reply(f'کاربر [{get_author.username}]({author_guid}) از گروه خارج شد!',
                         parse_mode='markdown')
        elif event_data.type == 'JoinedGroupByLink':
            update.reply(f'کاربر [{get_author.username}]({author_guid}) با استفاده از لینک به گروه وارد شد.',
                         parse_mode='markdown')
        elif event_data.type == 'RemoveGroupMembers':
            update.reply(f'کاربر [{get_author.username}]({author_guid}) از گروه حذف شد.',
                         parse_mode='markdown')
        elif event_data.type == 'PinnedMessageUpdated':
            update.reply('پیام سنجاق شده را مشاهده کنید.')
        else:
            update.reply(f'کاربر [{get_author.username}]({author_guid}) به گروه افزوده شد.',
                         parse_mode='markdown')

def add_group(update: Updates):
    return AddGroup(bot, session, update)

def lock_options(update: Updates):
    return SetLock(session, update)

def get_status(update: Updates):
    return GetStatus(update, session)

def is_ads(update: Updates):
    return IsAds(session, update)

def save_user_info(update: Updates) -> None:
    group = session.query(Group).filter_by(group_guid=update.object_guid).first()
    if group:
        """ذخیره اطلاعات کاربر در صورت عدم وجود در دیتابیس"""
        user_id = update.author_guid
        user = session.query(User).filter_by(user_guid=str(user_id)).first()

        if not user:
            # اگر کاربر در دیتابیس وجود نداشته باشد، اطلاعات او را ذخیره کن
            get_author = update.get_author()
            username = get_author.username
            user = User(user_guid=update.author_guid, username=username)
            session.add(user)
            session.commit()

bot.add_handler(
    func=save_user_info,
    handler=handlers.MessageUpdates(filters.is_group))
bot.add_handler(
    func=handle_events,
    handler=handlers.MessageUpdates(is_event))
bot.add_handler(
    func=handle_hyperlinks,
    handler=handlers.MessageUpdates(is_hyperlink))
bot.add_handler(
    func=handle_mention_text,
    handler=handlers.MessageUpdates(is_mention_text))
bot.add_handler(
    func=is_ads,
    handler=handlers.MessageUpdates(filters.is_group, filters.raw_text))
bot.add_handler(
    func=get_status,
    handler=handlers.MessageUpdates(filters.is_group, filters.RegexModel(r'status|وضعیت')))
bot.add_handler(
    func=lock_options,
    handler=handlers.MessageUpdates(filters.is_group, filters.RegexModel('^قفل')))
bot.add_handler(
    func=add_group,
    handler=handlers.MessageUpdates(filters.is_private, filters.RegexModel('^افزودن')))

bot.run()