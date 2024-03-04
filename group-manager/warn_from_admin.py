from rubpy.types import Update
from rubpy.enums import ParseMode
import database

def HandleWarns(update: Update, session: "database.Session"):
        if update.reply_message_id:
            author_guid = update.get_messages(message_ids=update.reply_message_id).messages[0].author_object_guid

        else:
            author_guid = update.client.get_info(username=update.text.split()[-1]).user_guid

        user = session.query(database.User).filter_by(user_guid=author_guid).first()
        if user:
            warnings_count = session.query(database.Warning).filter_by(group_guid=update.object_guid, user_guid=author_guid).count()
            if warnings_count >= 2:
                banned_user = database.BannedUser(group_guid=update.object_guid, user_guid=author_guid)
                session.add(banned_user)

                # حذف تمام اخطارهای قبلی این کاربر
                session.query(database.Warning).filter_by(group_guid=update.object_guid, user_guid=author_guid).delete()
                session.commit()

                update.ban_member(user_guid=author_guid)
                update.reply(f"کاربر [@{user.username}]({author_guid}) به دلیل دریافت 3 اخطار بن شد.",
                            parse_mode=ParseMode.MARKDOWN)

            else:
                warning = database.Warning(group_guid=update.object_guid, user_guid=author_guid, reason='اخطار از طرف ادمین')
                session.add(warning)
                session.commit()

                update.reply(f"[@{user.username}]({author_guid})\nاخطار - اخطار از طرف ادمین - /قوانین\nتعداد اخطارها تاکنون: {warnings_count + 1}",
                            parse_mode=ParseMode.MARKDOWN)