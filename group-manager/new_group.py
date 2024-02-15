from rubpy.types import Updates
from rubpy.utils import get_group_links
from rubpy import Client
from database import Group, Session

def AddGroup(
        client: Client,
        session: "Session",
        update: Updates,
):
    group_link = get_group_links(update.raw_text)[0]
    preview = client.group_preview_by_join_link(group_link)

    if not preview.is_valid:
        return update.reply('لینک گروه اشتباهه! 🙁')

    group_guid = preview.group.group_guid
    group_title = preview.group.group_title

    # بررسی وجود گروه با استفاده از `group_guid`
    existing_group = session.query(Group).filter_by(group_guid=group_guid).first()

    if existing_group:
        return update.reply(f'گروه 「{group_title}」از قبل اضافه شده! 😊')

    else:
        # ایجاد گروه جدید
        client.join_group(group_link)
        new_group = Group(group_guid=group_guid, name=group_title)
        session.add(new_group)
        session.commit()
        client.send_message(
            object_guid=group_guid,
            text='ربات با موفقیت در گروه فعال شد، لطفا حتما ربات را در گروه فول ادمین کنید در غیر اینصورت ربات به درستی کار نمیکند.\n\nبزرگترین گروه برنامه نویسی در روبیکا:\nhttps://rubika.ir/joing/EBCIHEDF0OPCSKJGOYILJWWJWOSEQRNB',
        )
        return update.reply(f'گروه 「{group_title}」رو اضافه کردم! 😁')