from rubpy import Client, handlers, filters, utils
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

def handle_events(update: Updates):
    group = session.query(Group).filter_by(group_guid=update.object_guid).first()
    if group:
        event_data = update.event_data
        get_author = update.get_author(event_data.object_guid)
        if event_data.type == 'LeaveGroup':
            update.reply(f'کاربر [{get_author.username}]({event_data.object_guid}) از گروه خارج شد!',
                         parse_mode='markdown')
        elif event_data.type == 'JoinedGroupByLink':
            update.reply(f'کاربر [{get_author.username}]({event_data.object_guid}) با استفاده از لینک به گروه وارد شد.',
                         parse_mode='markdown')
        elif event_data.type == 'RemoveGroupMembers':
            update.reply(f'کاربر [{get_author.username}]({event_data.object_guid}) از گروه حذف شد.',
                         parse_mode='markdown')
        else:
            update.reply(f'کاربر [{get_author.username}]({event_data.object_guid}) به گروه افزوده شد.',
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
    handler=handlers.MessageUpdates(is_event),
)
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