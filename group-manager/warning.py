<<<<<<< HEAD
from rubpy.types import Updates
from rubpy.enums import ParseMode
import database

def warn_user(update: Updates, session: "database.Session", reason='تبلیغ') -> None:
    """اخطار دادن به یک کاربر در گروه"""
    # استخراج مشخصات کاربر از پیام
    user_guid = update.author_guid
    user = session.query(database.User).filter_by(user_guid=user_guid).first()

    if user:
        # چک کردن تعداد اخطارهای کاربر
        warnings_count = session.query(database.Warning).filter_by(group_guid=update.object_guid, user_guid=user_guid).count()

        # اگر تعداد اخطارها به 3 برسد، کاربر را بن کرده و به لیست سیاه اضافه می‌کنیم
        if warnings_count >= 2:
            banned_user = database.BannedUser(group_guid=update.object_guid, user_guid=user_guid)
            session.add(banned_user)

            # حذف تمام اخطارهای قبلی این کاربر
            session.query(database.Warning).filter_by(group_guid=update.object_guid, user_guid=user_guid).delete()
            session.commit()

            #update.ban_member(user_guid=update.author_guid)
            update.reply(f"کاربر [@{user.username}]({update.author_guid}) به دلیل دریافت 3 اخطار بن شد.",
                         parse_mode=ParseMode.MARKDOWN)
        else:
            # ایجاد یک اخطار برای کاربر
            warning = database.Warning(group_guid=update.object_guid, user_guid=user_guid, reason=reason)
            session.add(warning)
            session.commit()

            update.reply(f"[@{user.username}]({update.author_guid})\nاخطار - {reason} - /قوانین\nتعداد اخطارها تاکنون: {warnings_count + 1}",
                         parse_mode=ParseMode.MARKDOWN)
=======
from rubpy.types import Updates
from rubpy.enums import ParseMode
import database

def warn_user(update: Updates, session: "database.Session", reason='تبلیغ') -> None:
    """اخطار دادن به یک کاربر در گروه"""
    # استخراج مشخصات کاربر از پیام
    user_guid = update.author_guid
    user = session.query(database.User).filter_by(user_guid=user_guid).first()

    if user:
        # چک کردن تعداد اخطارهای کاربر
        warnings_count = session.query(database.Warning).filter_by(group_guid=update.object_guid, user_guid=user_guid).count()

        # اگر تعداد اخطارها به 3 برسد، کاربر را بن کرده و به لیست سیاه اضافه می‌کنیم
        if warnings_count >= 2:
            banned_user = database.BannedUser(group_guid=update.object_guid, user_guid=user_guid)
            session.add(banned_user)

            # حذف تمام اخطارهای قبلی این کاربر
            session.query(database.Warning).filter_by(group_guid=update.object_guid, user_guid=user_guid).delete()
            session.commit()

            update.ban_member(user_guid=update.author_guid)
            update.reply(f"کاربر [@{user.username}]({update.author_guid}) به دلیل دریافت 3 اخطار بن شد.",
                         parse_mode=ParseMode.MARKDOWN)
        else:
            # ایجاد یک اخطار برای کاربر
            warning = database.Warning(group_guid=update.object_guid, user_guid=user_guid, reason=reason)
            session.add(warning)
            session.commit()

            update.reply(f"[@{user.username}]({update.author_guid})\nاخطار - {reason} - /قوانین\nتعداد اخطارها تاکنون: {warnings_count + 1}",
                         parse_mode=ParseMode.MARKDOWN)
>>>>>>> ae03d7c0e03114d91bd2c2b97b61e921e2a0a533
