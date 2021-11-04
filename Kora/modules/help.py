from Kora import CMD_HELP
from Kora import bot
from telethon import events


@bot.on(events.NewMessage(outgoing=True, pattern="^[?.]help(?: |$)(.*)"))
async def help(event):
    """ For ?help command,"""
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit("Please specify a valid module name.")
    else:
        string = ""
        for i in CMD_HELP:
            string += "`" + str(i)
            string += "`\t\t\t||\t\t\t "
        await event.edit(
            f"{string}"
            "\n\nSpecify which module do you want help for !!\
                        \n**Usage:** `?help` <module name>"
        )