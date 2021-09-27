from telethon import events
from config import bot
import m3u8_To_MP4
import logging
from FastTelethonhelper import fast_upload
import os
import subprocess
import asyncio

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                    level=logging.INFO)


@bot.on(events.NewMessage(pattern="/start"))
async def _(event):
    await event.reply("Hello!")

@bot.on(events.NewMessage(pattern="/download"))
async def _(event):
    try:
        txt_file = await event.get_reply_message()
        x = await bot.download_media(txt_file)
        with open(x) as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split(":", 1))
        os.remove(x)
    except:
        await event.reply("Invalid file input.")
        os.remove(x)
        return
        
    for i in links:
        name = i[0].split("\t")
        file_name = f"{name[1][:60]}.mkv"
        r = await event.reply(f"`Downloading...\n{name[1]}\n\nfile number: {name[0][:-1]}`")
        m3u8_To_MP4.download(i[1], mp4_file_name=file_name)
        try:
            os.remove("thumbnail.jpg")
        except:
            pass
        await asyncio.sleep(5)
        file = await fast_upload(bot, file_name, reply= r)
        subprocess.call(f'ffmpeg -i "{file_name}" -ss 00:00:01 -vframes 1 "thumbnail.jpg"', shell=True)
        await bot.send_message(event.chat_id, f"`{name[1]}\n\nfile number: {name[0][:-1]}`", file=file, force_document=False, thumb="thumbnail.jpg")
        os.remove(file_name)
        os.remove("thumbnail.jpg")
        await r.delete()
        break


bot.start()

bot.run_until_disconnected()
