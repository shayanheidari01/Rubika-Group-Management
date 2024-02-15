from rubpy.types import Updates
from rubpy import utils
from warning import warn_user
import database

def IsAds(
        session: "database.Session",
        update: Updates,
):
    group = session.query(database.Group).filter_by(group_guid=update.object_guid).first()
    if group:
        if update.is_admin() is False:
            if group.lock_usernames and utils.is_username(update.raw_text):
                update.delete_messages()
                author = update.get_author()
                return warn_user(update, session)
                return update.reply(f'کاربر [{update.author_guid}]({author.first_name}) نام کاربری فرستاد و پاک شد.',
                                    parse_mode='markdown')

            else:
                if group.lock_links:
                    if utils.is_group_link(update.raw_text):
                        update.delete_messages()
                        author = update.get_author()
                        return warn_user(update, session)
                        return update.reply(f'کاربر [{author.first_name}]({update.author_guid}) لینک گروه فرستاد و پاک شد.',
                                     parse_mode='markdown')

                    elif utils.is_rubika_link(update.raw_text):
                        update.delete_messages()
                        author = update.get_author()
                        return warn_user(update, session)
                        return update.reply(f'کاربر [{author.first_name}]({update.author_guid}) لینک روبیکا فرستاد و پاک شد.',
                                     parse_mode='markdown')