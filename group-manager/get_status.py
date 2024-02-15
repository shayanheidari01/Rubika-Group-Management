from rubpy.types import Updates
from rubpy.enums import ParseMode
from database import Session, Group

lock_types = [
    ("لینک", "links"),
    ("هایپرلینک", "hyperlinks"),
    ("نام کاربری", "usernames"),
    ("هشتگ", "hashtags"),
    ("متن (محدوده)", "text"),
    ("فحش", "badwords"),
    ("فوروارد", "forward"),
    ("اینلاین", "inline"),
    ("احراز هویت", "authentication"),
    ("ایموجی", "emojis"),
    ("فایل‌ها", "files"),
    ("عکس‌ها", "photos"),
    ("ویدیوها", "videos"),
    ("ویس‌ها", "audios"),
    ("گیف‌ها", "gifs"),
    ("استیکرها", "stickers"),
    ("مکان", "location"),
    ("مخاطب", "contact"),
    ("دستورات استیکر", "sticker_commands"),
    ("دستورات مدیا", "media_commands"),
    ("دستورات ویس", "voice_commands"),
    ("منشن دستور", "command_mention"),
    ("ریپلای اسپویلر", "reply_spoiler"),
    ("نظرسنجی", "polls"),
    ("استوری", "story")
]

def GetStatus(update: Updates, session: "Session") -> None:
    """نمایش وضعیت قفل‌ها در گروه به صورت فارسی"""
    group = session.query(Group).filter_by(group_guid=update.object_guid).first()

    if group:
        status_message = '🔷 **وضعیت قفل ها:**\n\n'
        for lock_name, lock_type in lock_types:
            lock_status = "✅" if getattr(group, f"lock_{lock_type}") else "❌"
            status_message += f"• {lock_name}: {lock_status}\n"

        update.reply(status_message, parse_mode=ParseMode.MARKDOWN)