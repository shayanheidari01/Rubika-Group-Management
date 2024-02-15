from rubpy.types import Updates
from rubpy.enums import ParseMode
from database import Group, Session

lock_types = [
    ("لینک", "links"),
    ("هایپرلینک", "hyperlinks"),
    ("نام کاربری", "usernames"),
    ("هشتگ", "hashtags"),
    ("متن", "text"),
    ("فحش", "badwords"),
    ("فوروارد", "forward"),
    ("اینلاین", "inline"),
    ("احراز هویت", "authentication"),
    ("ایموجی", "emojis"),
    ("فایل", "files"),
    ("عکس", "photos"),
    ("ویدیو", "videos"),
    ("ویس", "audios"),
    ("گیف", "gifs"),
    ("استیکر", "stickers"),
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

def SetLock(
        session: "Session",
        update: Updates,
):
    """تنظیم قفل موردنظر در گروه"""
    group = session.query(Group).filter_by(group_guid=update.object_guid).first()
    lock_type = update.raw_text.replace('قفل', '').strip()
    lock_name = None

    if group:
        if not lock_type:
            update.reply("لطفاً نوع قفل را وارد کنید. برای مثال: `قفل لینک`", parse_mode=ParseMode.MARKDOWN)
            return

        for lock_name, type in lock_types:
            if lock_name == lock_type:
                lock_type = type
                lock_name = lock_name
                break
            else:
                lock_name = None

        if hasattr(group, f"lock_{lock_type}"):
            # تغییر وضعیت قفل موردنظر
            current_lock_status = getattr(group, f"lock_{lock_type}")
            setattr(group, f"lock_{lock_type}", not current_lock_status)

            session.commit()
            lock_status_str = "فعال" if getattr(group, f"lock_{lock_type}") else "غیرفعال"
            update.reply(f"قفل {lock_name or lock_type} با موفقیت {lock_status_str} شد.")

        else:
            update.reply("نوع قفل نامعتبر است.")