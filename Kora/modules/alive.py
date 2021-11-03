from Kora import ALIVE_NAME, CMD_HELP, ALIVE_LOGO
from platform import python_version, uname
from telethon import version
import asyncio
from Kora.events import kora
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node

modules = CMD_HELP


@kora(outgoing=True, pattern="^?alive")
async def alivekora(alive):
    user = await bot.get_me()
    await alive.edit("`hey, you have doubt? ohh shit...`")
    await alive.edit("`i'm really alive re`")

    text = (
        f" **__KORA USERBOT__** \n\n"
        f"**Owner** \n"
        f" ➥ `{DEFAULTUSER}` \n"
        f"**♛ ᴜsᴇʀɴᴀᴍᴇ** \n"
        f" ➥ `@{user.username}` \n"
        f"┏━━━━━━━━━━━━━━━━━━━\n"
        f"┣[• `Telethon :`Ver {version.__version__} \n"
        f"┣[• `Python   :`Ver {python_version()} \n"
        f"┣[• `Modules  :`{len(modules)} Modules \n"
        f"┗━━━━━━━━━━━━━━━━━━━")
    if ALIVE_LOGO:
        try:
            logo = ALIVE_LOGO
            await alive.delete()
            msg = await bot.send_file(alive.chat_id, logo, caption=text)
            await asyncio.sleep(200)
            await msg.delete()
        except BaseException:
            await alive.edit(
                text + "\n\n *`The provided logo is invalid."
                "\nMake sure the link is directed to the logo picture`"
            )
            await asyncio.sleep(200)
            await alive.delete()
    else:
        await alive.edit(text)
        await asyncio.sleep(200)
        await alive.delete()
