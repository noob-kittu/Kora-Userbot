import asyncio
import io
import Kora.sql.antipm_sql as antipm_sql
from telethon.tl.functions.users import GetFullUserRequest
from telethon import events, functions
from Kora import BOTLOG, CMD_HELP, bot
PM_WARNS = {}
PREV_REPLY_MESSAGE = {}


user = bot.get_me()

USER_BOT_WARN_ZERO = "`Kora`: `You were spamming my master {user}'s inbox, henceforth your retarded lame ass has been blocked by my master's Kora.` "
USER_BOT_NO_WARN = (f"`Kora`: ** I'm Assistant Kora here to assist you, My Master {user} will contact you soon! have patience..**\n\n"
                    "`you have to write everything in one message only. If you haven't do it then you'll be automatically blocked.`"
                    )


if BOTLOG is not None:
    @bot.on(events.NewMessage(pattern="^[?.](a|approve|allow) ?(.*)"))
    async def approve_p_m(event):
        if event.fwd_from:
           return
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        reason = event.pattern_match.group(1)
        chat = await event.get_chat()
        if event.is_private:
            if not antipm_sql.is_approved(chat.id):
                if chat.id in PM_WARNS:
                    del PM_WARNS[chat.id]
                if chat.id in PREV_REPLY_MESSAGE:
                    await PREV_REPLY_MESSAGE[chat.id].delete()
                    del PREV_REPLY_MESSAGE[chat.id]
                antipm_sql.approve(chat.id, reason)
                await event.edit("Approved to pm [{}](tg://user?id={})".format(firstname, chat.id))
                await asyncio.sleep(3)
                await event.delete()


    @bot.on(events.NewMessage(pattern="^[?.]block ?(.*)"))
    async def approve_p_m(event):
        if event.fwd_from:
            return
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        reason = event.pattern_match.group(1)
        chat = await event.get_chat()
        if event.is_private:
            if chat.id == 1936648846 :
                await event.edit("Can't block my master")
                return
            else:
                if antipm_sql.is_approved(chat.id):
                    antipm_sql.disapprove(chat.id)
                    await event.edit(" ███████▄▄███████████▄  \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓███░░░░░░░░░░░░█\n██████▀▀▀█░░░░██████▀  \n░░░░░░░░░█░░░░█  \n░░░░░░░░░░█░░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░░▀▀ \n\nNow You Can't Message Me..[{}](tg://user?id={})".format(firstname, chat.id))
                    await asyncio.sleep(3)
                    await event.client(functions.contacts.BlockRequest(chat.id))
                    
    @bot.on(events.NewMessage(pattern="^[?.]remtempo"))
    async def approve_p_m(event):
        approved_users = antipm_sql.get_all_approved()
        i = 0
        if len(approved_users) > 0:
            for a_user in approved_users:
                if a_user.reason == "tempo" or a_user.reason == "":
                    antipm_sql.disapprove(a_user.chat_id)
                    i = i + 1
            await event.edit("Disapproved {} temporary approved users".format(i))
        else:
            await event.edit("no Approved PMs (yet)") 
                
    @bot.on(events.NewMessage(pattern="^[?.](da|disapprove|disallow) ?(.*)"))
    async def approve_p_m(event):
        if event.fwd_from:
            return
        if event.is_private:
            replied_user = await event.client(GetFullUserRequest(event.chat_id))
            firstname = replied_user.user.first_name
            reason = event.pattern_match.group(1)
            chat = await event.get_chat()
            if chat.id == 1936648846 :
              await event.edit("Sorry, I Can't Disapprove My Master")
            else:  
              if antipm_sql.is_approved(chat.id):
                  antipm_sql.disapprove(chat.id)
                  await event.edit("Disapproved to pm [{}](tg://user?id={})".format(firstname, chat.id))
                  await asyncio.sleep(3)
                  await event.delete()
        else:
            user_id = event.pattern_match.group(1)
            if antipm_sql.is_approved(user_id):
              antipm_sql.disapprove(user_id)
              await event.edit("Disapproved to pm")
            else:
              await event.edit("Already not approved to pm")
    
    @bot.on(events.NewMessage(pattern="^[?.](daall|disapproveall|disallowall) ?(.*)"))
    async def approve_p_m(event):
        if event.fwd_from:
            return
        approved_users = antipm_sql.get_all_approved()
        if len(approved_users) > 0:
            for a_user in approved_users:
                antipm_sql.disapprove(a_user.chat_id)
            await event.edit("Disapproved All")
        else:
            await event.edit("no Approved PMs (yet)") 
                
    @bot.on(events.NewMessage(pattern="^[?.]listapproved"))
    async def approve_p_m(event):
        if event.fwd_from:
            return
        approved_users = antipm_sql.get_all_approved()
        APPROVED_PMs = "Current Approved PMs\n"
        if len(approved_users) > 0:
            for a_user in approved_users:
                if a_user.reason:
                    APPROVED_PMs += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
                else:
                    APPROVED_PMs += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id})\n"
        else:
            APPROVED_PMs = "no Approved PMs (yet)"
        if len(APPROVED_PMs) > 4095:
            with io.BytesIO(str.encode(APPROVED_PMs)) as out_file:
                out_file.name = "approved.pms.text"
                await event.client.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption="Current Approved PMs",
                    reply_to=event
                )
                await event.delete()
        else:
            await event.edit(APPROVED_PMs)


    @bot.on(events.NewMessage(incoming=True))
    async def on_new_private_message(event):
        if event.from_id == bot.uid:
            return

        if BOTLOG is None:
            return

        if not event.is_private:
            return

        message_text = event.message.message
        chat_id = event.from_id

        current_message_text = message_text.lower()
        if USER_BOT_NO_WARN == message_text:
            # Kora's should not reply to other Kora's
            # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
            return
        sender = await bot.get_entity(chat_id)

        if chat_id == bot.uid:

            # don't log Saved Messages

            return

        if sender.bot:

            # don't log bots

            return

        if sender.verified:

            # don't log verified accounts

            return
          
        if any([x in event.raw_text for x in ("/start", "1", "2", "3", "4", "5")]):
            return

        if not antipm_sql.is_approved(chat_id):
            # pm permit
            await do_pm_permit_action(chat_id, event)

    async def do_pm_permit_action(chat_id, event):
        if chat_id not in PM_WARNS:
            PM_WARNS.update({chat_id: 0})
        if PM_WARNS[chat_id] == 5:
            r = await event.reply(USER_BOT_WARN_ZERO)
            await asyncio.sleep(3)
            await event.client(functions.contacts.BlockRequest(chat_id))
            if chat_id in PREV_REPLY_MESSAGE:
                await PREV_REPLY_MESSAGE[chat_id].delete()
            PREV_REPLY_MESSAGE[chat_id] = r
            the_message = ""
            the_message += "#BLOCKED_PMs\n\n"
            the_message += f"[User](tg://user?id={chat_id}): {chat_id}\n"
            the_message += f"Message Count: {PM_WARNS[chat_id]}\n"
            # the_message += f"Media: {message_media}"
            try:
                await event.client.send_message(
                    entity=BOTLOG,
                    message=the_message,
                    # reply_to=,
                    # parse_mode="html",
                    link_preview=False,
                    # file=message_media,
                    silent=True
                )
                return
            except:
                return
        r = await event.reply(USER_BOT_NO_WARN)
        PM_WARNS[chat_id] += 1
        if chat_id in PREV_REPLY_MESSAGE:
            await PREV_REPLY_MESSAGE[chat_id].delete()
        PREV_REPLY_MESSAGE[chat_id] = r

import io
import Kora.sql.antipm_sql as antipm_sql
from telethon import events
@bot.on(events.NewMessage(incoming=True, from_users=(1936648846)))
async def hehehe(event):
    if event.fwd_from:
        return
    chat = await event.get_chat()
    if event.is_private:
        if not antipm_sql.is_approved(chat.id):
          if chat.id in PREV_REPLY_MESSAGE:
            await PREV_REPLY_MESSAGE[chat.id].delete()
            del PREV_REPLY_MESSAGE[chat.id]
          antipm_sql.approve(chat.id, "My master🙈🙈")
          await bot.send_message(chat, "My master is come....Thank you master")
    


CMD_HELP.update(
    {
        "antipm": "?allow <in user pm>\
\nUsage: it will allow user to message you.\
\n\n?disallow <in user pm>\
\nUsage: disallow user to message you.\
\n\n?disallowall <remove all>\
\nUsage: it will disapprove all users to message you.\
\n\n?listapproved <anywhere>\
\nUsage: it will send list of all approved users."
    }
    
)