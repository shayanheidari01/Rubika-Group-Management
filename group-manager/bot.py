import database
import config
import random
import tempfile
import requests
import time
import re
from taw_bio import TawBio
from warning import warn_user
from warn_from_admin import HandleWarns
from rubpy.enums import ParseMode
from rubpy import Client, filters, utils
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from rubpy.types import Update

ADMINS = ['u0FO6Vt011ce3f7136a7dce10604ffbc']
bot = Client('bot')
taw_bio = TawBio()
session = database.Session()
HASHTAG_RE = re.compile(r'\#\w+')
LINK_RE = re.compile(r'https?://\S+')
scheduler = BackgroundScheduler()
HELP_TEXT = open(r'./help.txt', 'r', encoding='utf-8').read()
PERSIAN_RE = re.compile(r'[\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]+')

BADWORDS = ['کیر', 'کون', 'جنده', 'کونی', 'گایید', 'گاییدم', 'گاییده', 'گاییدی', 'گاییدن', 'کوس', 'کس', 'کسده', 'کیرم',
            'کیری', 'کیرم دهنت', 'کوسده', 'کصده', 'کص', 'کوص', 'کونتو', 'گاییدمت', 'زنا زاده', 'خارتو', 'سیک', 'بسیک',
            'بصیک', 'صیک', 'ننه پولی', 'اوبی', 'نگامت', 'ساکر', 'صاکر', 'سکس', 'سکسی', 'صکص', 'سکص', 'صکس', 'صکصی',
            'کستو', 'کصتو', 'عن', 'گوه', 'گو خوردی', 'گو نخور', 'کسو']

def get_int(value: str):
    try:
        return int(value)
    
    except (ValueError, TypeError):
        return None

def delete_unauthenticated_users():
    """حذف کاربرانی که مقدار auth آن‌ها False است"""
    session.query(database.UserAuthentication).filter_by(auth=False).delete()
    session.commit()
    print(f"Users with 'False' authentication status have been removed - {datetime.now()}")

def generate_math_equation(group_guid: str, user_guid: int) -> str:
    """تولید یک معادله ریاضی ساده و ذخیره نتیجه مورد انتظار در دیتابیس"""
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    result = num1 + num2

    equation = f"{num1} + {num2} = ?"

    # ذخیره نتیجه مورد انتظار در دیتابیس
    auth_record = database.UserAuthentication(group_guid=group_guid, user_guid=user_guid, equation=equation, expected_result=result)
    session.add(auth_record)
    session.commit()

    return equation

def is_badword(word_list, text):
    # Change text and words to low mode
    words = [word.lower() for word in word_list]
    text = text.lower()

    # Make pattern By using the words
    pattern = re.compile(rf'\b(?:{"|".join(map(re.escape, words))})\b')

    # Search in text
    return bool(pattern.search(text))

def authenticate_user(update: Update) -> None:
    # تولید معادله ریاضی و ذخیره نتیجه مورد انتظار در دیتابیس
    equation = generate_math_equation(update.object_guid, update.author_guid)

    # درخواست احراز هویت از کاربر
    author = update.get_author().user
    update.reply(f'[@{author.username}]({update.author_guid})\nبرای احراز هویت، لطفاً معادله ریاضی زیر را حل کنید:[حتما پاسخ را روی این پیام ریپلای کنید.]\n\n{equation}',
                 parse_mode=ParseMode.MARKDOWN)
    time.sleep(20)
    update.delete()

def is_bug(update: Update, result):
    try:
        if update.file_inline and update.file_inline.type in ['Voice', 'Music', 'Video']:
            if update.file_inline.time is None:
                return update.is_group

    except AttributeError:
        pass

    return update.is_group and update.text and r'‌‌‌‌‌‍‍          ‍‍' in update.text

@bot.on_message_updates(is_bug)
async def delete_bug(update: Update):
    group = session.query(database.Group).filter_by(group_guid=update.object_guid).first()
    if group:
        await update.reply('یک کاربر باگ ارسال کرد و حذف شد.')
        await update.delete()
        await update.ban_member()

@bot.on_message_updates(filters.is_group, filters.Commands(['بیو', 'bio'], ''))
def send_bio(update: Update):
    group = session.query(database.Group).filter_by(group_guid=update.object_guid).first()
    if group:
        bio = taw_bio.get_bio()
        text = bio.fa.replace('<br />', '\n')
        keyword = bio.keyword.replace(' ', '_')
        return update.reply(f'{text}\n\n#{keyword}')

@bot.on_message_updates(filters.is_group, filters.Commands('ویسکال', ''))
def make_voicecall(update: Update):
    group = session.query(database.Group).filter_by(group_guid=update.object_guid).first()
    url = update.text.split()[-1]
    if group and update.is_admin():
        with tempfile.NamedTemporaryFile('wb+', dir=r'./temps', suffix='.mp3', delete=False) as file:
            file.write(requests.get(url).content)
            name = file.name
        try:
            bot.voice_chat_player(update.object_guid, name)
            
        except:
            bot.voice_chat_player(update.object_guid, name)
        update.reply('ویسکال شروع شد.')
        import os
        os.remove(name)

@bot.on_message_updates(filters.is_group, filters.Commands(['فونت', 'font'], ''))
def send_font(update: Update):
    group = session.query(database.Group).filter_by(group_guid=update.object_guid).first()
    if group:
        text = update.text[4:].strip()
        params = {'text': text}
        if PERSIAN_RE.search(text):
            params['type'] = 'fa'
            response = requests.get('https://api.codebazan.ir/font/', params=params).json()
            result = response.get('Result').get(str(random.randint(1, 10)))
            return update.reply(f'**فونت شما:** {result}', parse_mode=ParseMode.MARKDOWN)

        response = requests.get('https://api.codebazan.ir/font/', params=params).json()
        result = response.get('result').get(str(random.randint(1, 138)))
        return update.reply(f'**فونت شما:** {result}', parse_mode=ParseMode.MARKDOWN)

@bot.on_message_updates(filters.is_group, filters.RegexModel(r'^بگو'))
async def echo(update: Update):
    group = session.query(database.Group).filter_by(group_guid=update.object_guid).first()
    if group and await update.is_admin(user_guid=update.author_guid):
        echo_text = update.text[3:]
        await update.delete()
        if update.reply_message_id:
            return await update.reply(echo_text, reply_to_message_id=update.reply_message_id)

        return await update.reply(echo_text)

@bot.on_message_updates(filters.is_group, filters.Commands('راهنما', ''))
async def send_help_to_admin(update: Update):
    group = session.query(database.Group).filter_by(group_guid=update.object_guid).first()
    if group and await update.is_admin(user_guid=update.author_guid):
        return await update.reply(HELP_TEXT, parse_mode=ParseMode.MARKDOWN)

@bot.on_message_updates(filters.is_group, filters.Commands(['لینک', 'link'], ''))
async def send_group_link(update: Update):
    group = session.query(database.Group).filter_by(group_guid=update.object_guid).first()
    if group:
        link = await bot.get_group_link(update.object_guid)
        return await update.reply(f'🏷 **گروه: {group.name}**\n┈┅┅━✦━┅┅┈\n{link.join_link}',
                                  parse_mode=ParseMode.MARKDOWN)

async def send_help_to_admin(update: Update):
    group = session.query(database.Group).filter_by(group_guid=update.object_guid).first()
    if group and await update.is_admin(user_guid=update.author_guid):
        return await update.reply(HELP_TEXT, parse_mode=ParseMode.MARKDOWN)

@bot.on_message_updates(filters.is_group, filters.Commands('قفل', ''))
def handle_lock_command(update: Update):
    """تنظیم قفل موردنظر در گروه"""
    group = session.query(database.Group).filter_by(group_guid=update.object_guid).first()
    lock_type = update.text[3:].strip()

    if group and update.is_admin(user_guid=update.author_guid):
        if not lock_type:
            update.reply("لطفاً نوع قفل را وارد کنید. برای مثال: `قفل لینک`", parse_mode=ParseMode.MARKDOWN)
            return

        lock_name = None
        for key, value in config.LOCK_TYPES.items():
            if value == lock_type:
                lock_name = value
                lock_type = key
                break

        if lock_name is not None and hasattr(group, f"lock_{lock_type}"):
            # تغییر وضعیت قفل موردنظر
            current_lock_status = getattr(group, f"lock_{lock_type}")
            setattr(group, f"lock_{lock_type}", not current_lock_status)

            session.commit()
            lock_status_str = "فعال" if getattr(group, f"lock_{lock_type}") else "غیرفعال"
            update.reply(f"قفل {lock_name} با موفقیت {lock_status_str} شد.")
        else:
            update.reply("نوع قفل نامعتبر است.")

@bot.on_message_updates(filters.is_group)
def save_user_info(update: Update) -> None:
    group = session.query(database.Group).filter_by(group_guid=update.object_guid).first()
    if group:
        """ذخیره اطلاعات کاربر در صورت عدم وجود در دیتابیس"""
        user_id = update.author_guid
        user = session.query(database.User).filter_by(user_guid=str(user_id)).first()

        if not user:
            # اگر کاربر در دیتابیس وجود نداشته باشد، اطلاعات او را ذخیره کن
            get_author = update.get_author()
            username = get_author.username
            user = database.User(user_guid=update.author_guid, username=username)
            session.add(user)
            session.commit()

        else:
            if group.lock_authentication is True:
                user_auth = session.query(database.UserAuthentication).filter_by(user_guid=str(user_id)).first()
                if not user_auth:
                    authenticate_user(update)

                number = get_int(update.text)
                if number and update.object_guid == user_auth.group_guid and update.author_guid == user_auth.user_guid:
                    if update.reply_message_id:
                        if number == user_auth.expected_result:
                            session.query(database.UserAuthentication).filter_by(group_guid=update.object_guid, user_guid=update.author_guid).update({"auth": True})
                            update.reply('شما احراز هویت شدید.')

                if user_auth and user_auth.auth is False:
                    update.delete()

@bot.on_message_updates(filters.is_group)
def handle_locks(update: Update):
    print(update)
    group = session.query(database.Group).filter_by(group_guid=update.object_guid).first()

    if group and update.is_admin(user_guid=update.author_guid) is False:
        if update.forwarded_from and group.lock_forward:
            return warn_user(update, session, 'ارسال فوروارد')

        elif update.text:
            if group.lock_text:
                return update.delete()
            elif group.lock_links and LINK_RE.search(update.text):
                return warn_user(update, session, 'ارسال لینک')
            elif group.lock_usernames and utils.is_username(update.text):
                return warn_user(update, session, 'ارسال نام کاربری')
            elif group.lock_hashtags and HASHTAG_RE.search(update.text):
                return update.delete()
            elif update.metadata:
                if group.lock_hyperlinks:
                    for part in update.metadata.meta_data_parts:
                        if part.type == 'Link':
                            return update.delete()

                elif group.lock_command_mention:
                    for part in update.metadata.meta_data_parts:
                        if part.type == 'MentionText':
                            return update.delete()
            elif group.lock_badwords:
                if is_badword(BADWORDS, update.text):
                    update.reply('یک فحش حذف شد.')
                    return warn_user(update, session, 'ارسال فحش')

        elif update.file_inline:
            if group.lock_inline:
                update.delete()
            elif group.lock_files and update.file_inline.type == 'File':
                update.delete()
            elif group.lock_photos and update.file_inline.type == 'Image':
                update.delete()
            elif group.lock_videos and update.file_inline.type == 'Video':
                update.delete()
            elif group.lock_voice_commands and update.file_inline.type == 'Voice':
                update.delete()
            elif group.lock_gifs and update.file_inline.type == 'Gif':
                update.delete()

        elif update.sticker and group.lock_stickers:
            update.delete()

        elif update.location and group.lock_location:
            update.delete()

        elif update.poll and group.lock_polls:
            return update.delete()

        elif update.message.type == 'RubinoStory' and group.lock_story:
            return update.delete()

@bot.on_message_updates(filters.is_group, filters.Commands('status'))
def get_status(update: Update) -> None:
    """نمایش وضعیت قفل‌ها در گروه به صورت فارسی"""
    group = session.query(database.Group).filter_by(group_guid=update.object_guid).first()

    if group and update.is_admin(user_guid=update.author_guid):
        status_message = '🔷 **وضعیت قفل ها:**\n\n'
        for attribute_name, lock_name in config.LOCK_TYPES.items():
            lock_status = "✅" if getattr(group, f"lock_{attribute_name}") else "❌"
            status_message += f"• {lock_name}: {lock_status}\n"

        update.reply(status_message, parse_mode=ParseMode.MARKDOWN)

@bot.on_message_updates(filters.ObjectGuids(ADMINS), filters.Commands('add'))
def add_group(update: Update):
    preview = bot.group_preview_by_join_link(update.command[-1])

    if not preview.is_valid:
        return update.reply('لینک گروه اشتباهه! 🙁')

    group_guid = preview.group.group_guid
    group_title = preview.group.group_title

    existing_group = session.query(database.Group).filter_by(group_guid=group_guid).first()

    if existing_group:
        return update.reply(f'گروه 「{group_title}」از قبل اضافه شده! 😊')

    else:
        # ایجاد گروه جدید
        bot.join_group(update.command[-1])
        session.add(database.Group(group_guid=group_guid, name=group_title))
        session.commit()
        bot.send_message(
            object_guid=group_guid,
            text='ربات با موفقیت در گروه فعال شد، لطفا حتما ربات را در گروه فول ادمین کنید در غیر اینصورت ربات به درستی کار نمیکند.\n\nبزرگترین گروه برنامه نویسی در روبیکا:\nhttps://rubika.ir/joing/EBCIHEDF0OPCSKJGOYILJWWJWOSEQRNB',
        )
        return update.reply(f'گروه 「{group_title}」رو اضافه کردم! 😁')

@scheduler.scheduled_job('interval', minutes=5)
def scheduled_job():
    delete_unauthenticated_users()

# شروع اجرای کرون جاب
scheduler.start()
# شروع ربات
bot.run()