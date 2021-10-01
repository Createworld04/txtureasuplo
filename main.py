from telethon import events
from config import bot, auth_groups, auth_users
import m3u8_To_MP4
import logging
from FastTelethonhelper import fast_upload
import os
import subprocess
import asyncio
import datetime
import downloader
import helper
from telethon.tl.types import DocumentAttributeVideo


logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                    level=logging.INFO)

cancel = False

@bot.on(events.NewMessage(pattern="/start", chats=auth_groups, from_users=auth_users))
async def _(event):
    await event.reply("Hello!")


@bot.on(events.NewMessage(pattern="/cancel", chats=auth_groups, from_users=auth_users))
async def _(event):
    global cancel
    cancel = True
    await event.reply("Trying to cancel all processes.")
    return


@bot.on(events.NewMessage(pattern="/download", chats=auth_groups, from_users=auth_users))
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
        try:
            if cancel == True:
                await event.reply("Process canceled")
                return
            name = links[i][0]
            file_name = f"{name[:60]}.mp4"
            r = await event.reply(f"`Downloading...\n{name[:60]}\n\nfile number: {i+1}`")
            if "m3u8" in links[i][1]:
                m3u8_To_MP4.download(links[i][1], mp4_file_name=file_name)
            else:
                await downloader.DownLoadFile(links[i][1], 1024*10, r, file_name=file_name)
                
            if os.path.exists("thumbnail.jpg"):
                os.remove("thumbnail.jpg")
            file = await fast_upload(bot, file_name, reply= r)
            subprocess.call(f'ffmpeg -i "{file_name}" -ss 00:00:01 -vframes 1 "thumbnail.jpg"', shell=True)
            dur = int(helper.duration(file_name))
            await bot.send_message(
                event.chat_id, f"`{name[:60]}\n\nfile number: {i+1}`", 
                file=file, 
                force_document=False, 
                thumb="thumbnail.jpg", 
                supports_streaming=True, 
                attributes=[DocumentAttributeVideo(duration=dur, w=1260, h=720, supports_streaming=True)])
            os.remove(file_name)
            os.remove("thumbnail.jpg")
            await r.delete()
        except Exception as e:
            print(e)
            pass
          
          
@bot.on(events.NewMessage(pattern="/upload", chats=auth_groups, from_users=auth_users))
async def _(event):
    arg = event.raw_text.split(" ", maxsplit = 1)[1]
    arg = arg.split("|")
    date = datetime.date.today()
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M%S")
    if len(arg) == 1:
        file_name = f"{date} {current_time}.mp4"
        caption = None
    else:
        file_name = arg[1].strip()
        caption = arg[1].strip()

    r = await event.reply("Trying do download.")
    try:
        if "m3u8" in arg[0]:
            m3u8_To_MP4.download(arg[0].strip(), mp4_file_name=file_name)
        else:
            await downloader.DownLoadFile(arg[0], 1024*10, r, file_name=file_name)

        if os.path.exists("thumbnail.jpg"):
            os.remove("thumbnail.jpg")

        await asyncio.sleep(5)
        file = await fast_upload(bot, file_name, reply= r)
        subprocess.call(f'ffmpeg -i "{file_name}" -ss 00:00:01 -vframes 1 "thumbnail.jpg"', shell=True)
        dur = int(helper.duration(file_name))
        await bot.send_message(
            event.chat_id,
            message=caption,
            file=file, 
            force_document=False, 
            thumb="thumbnail.jpg", 
            supports_streaming=True, 
            attributes=[DocumentAttributeVideo(duration=dur, w=1260, h=720, supports_streaming=True)])
        os.remove(file_name)
        os.remove("thumbnail.jpg")
        await r.delete()

    
    except Exception as e:
        print(e)
        await r.edit(f"File not downloaded/uploaded because of some error\nError:\n{e}")


@bot.on(events.NewMessage(pattern="/txt", chats=auth_groups, from_users=auth_users))
async def _(event):
    try:
        x = await event.get_reply_message()
        json_file = await bot.download_media(x)
        res, count = helper.parse_json_to_txt(json_file)
        await event.reply(f"{count} links detected." ,file=res)
        os.remove(json_file)
        os.remove(res)
    except:
        await event.reply("Invalid Json file input.")


@bot.on(events.NewMessage(pattern="/html", chats=auth_groups, from_users=auth_users))
async def _(event):
    try:
        x = await event.get_reply_message()
        json_file = await bot.download_media(x)
        res, count = helper.parse_json_to_html(json_file)
        await event.reply(f"{count} links detected." ,file=res)
        os.remove(json_file)
        os.remove(res)
    except Exception:
        await event.reply("Invalid Json file input.")


bot.start()

bot.run_until_disconnected()

