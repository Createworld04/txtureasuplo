from telethon import events
from config import bot
import m3u8_To_MP4
import logging
from FastTelethonhelper import fast_upload
import os
import subprocess
import asyncio
import datetime
import downloader

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                    level=logging.INFO)

cancel = False

@bot.on(events.NewMessage(pattern="/start"))
async def _(event):
    await event.reply("Hello!")


@bot.on(events.NewMessage(pattern="/cancel"))
async def _(event):
    global cancel
    cancel = True
    await event.reply("Trying to cancel all processes.")
    return


@bot.on(events.NewMessage(pattern="/download"))
async def _(event):
    global cancel
    cancel = False
    try:
        arg = int(event.raw_text.split(" ")[1])
        arg -= 1
    except:
        arg = 0
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
        
    for i in range(arg, len(links)):
        if cancel == True:
            await event.reply("Process canceled")
            return
        name = links[i][0].split("\t")
        file_name = f"{name[1][:60]}.mkv"
        r = await event.reply(f"`Downloading...\n{name[1]}\n\nfile number: {name[0][:-1]}`")
        m3u8_To_MP4.download(links[i][1], mp4_file_name=file_name)
        if os.path.exists("thumbnail.jpg"):
            os.remove("thumbnail.jpg")
        await asyncio.sleep(5)
        file = await fast_upload(bot, file_name, reply= r)
        subprocess.call(f'ffmpeg -i "{file_name}" -ss 00:00:01 -vframes 1 "thumbnail.jpg"', shell=True)
        await bot.send_message(event.chat_id, f"`{name[1]}\n\nfile number: {name[0][:-1]}`", file=file, force_document=False, thumb="thumbnail.jpg")
        os.remove(file_name)
        os.remove("thumbnail.jpg")
        await r.delete()


@bot.on(events.NewMessage(pattern="/upload"))
async def _(event):
    arg = event.raw_text.split(" ")[1]
    date = datetime.date.today()
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    file_name = f"{date} {current_time}.mp4"
    r = event.reply("Trying do download.")
    try:
        if "m3u8" in arg:
            m3u8_To_MP4.download(arg, mp4_file_name=file_name)
        else:
            await downloader.DownLoadFile(arg, 1024*10, r, file_name=file_name)

        if os.path.exists("thumbnail.jpg"):
            os.remove("thumbnail.jpg")
            
        await asyncio.sleep(5)
        file = await fast_upload(bot, file_name, reply= r)
        subprocess.call(f'ffmpeg -i "{file_name}" -ss 00:00:01 -vframes 1 "thumbnail.jpg"', shell=True)
        await bot.send_message(event.chat_id, file=file, force_document=False, thumb="thumbnail.jpg")
        os.remove(file_name)
        os.remove("thumbnail.jpg")
        await r.delete()

    
    except Exception as e:
        r.edit(f"File not downloaded/uploaded because of some error\nError:\n{e}")


bot.start()

bot.run_until_disconnected()


