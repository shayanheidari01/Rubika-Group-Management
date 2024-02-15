from rubpy.types import Updates
from rubpy.enums import ParseMode
from database import Group, User, Warning, BannedUser, Session  # این را به ماژول مدل‌های خود تغییر دهید

def warn_user(update: Updates, session: "Session", reason='تبلیغ') -> None:
    """اخطار دادن به یک کاربر در گروه"""
    chat_id = update.object_guid
    group = session.query(Group).filter_by(group_guid=str(chat_id)).first()

    if group:
        # استخراج مشخصات کاربر از پیام
        user_guid = update.author_guid
        user = session.query(User).filter_by(user_guid=user_guid).first()

        if user:
            # چک کردن تعداد اخطارهای کاربر
            warnings_count = session.query(Warning).filter_by(group_guid=str(chat_id), user_guid=user_guid).count()

            # اگر تعداد اخطارها به 3 برسد، کاربر را بن کرده و به لیست سیاه اضافه می‌کنیم
            if warnings_count >= 2:
                banned_user = BannedUser(group_guid=str(chat_id), user_guid=user_guid)
                session.add(banned_user)

                # حذف تمام اخطارهای قبلی این کاربر
                session.query(Warning).filter_by(group_guid=str(chat_id), user_guid=user_guid).delete()

                session.commit()

                update.ban_member(user_guid=update.author_guid)
                update.reply(f"کاربر [{user.username}]({update.author_guid}) به دلیل دریافت 3 اخطار بن شد.",
                             parse_mode=ParseMode.MARKDOWN)
            else:
                # ایجاد یک اخطار برای کاربر
                warning = Warning(group_guid=str(chat_id), user_guid=user_guid, reason=reason)
                session.add(warning)
                session.commit()

                update.reply(f"کاربر [{user.username}]({update.author_guid}) با موفقیت اخطار داده شد.",
                             parse_mode=ParseMode.MARKDOWN)