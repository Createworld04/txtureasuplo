from telethon import events, Button
from config import bot#, auth_groups, auth_users
import logging
from FastTelethonhelper import fast_upload
import os
import subprocess
import helper
from telethon.tl.types import DocumentAttributeVideo


logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                    level=logging.INFO)

cancel = False

# @bot.on(events.NewMessage(pattern="/start"))
# async def _(event):
#     if event.is_private:
#         if event.sender_id not in auth_users:
#             return
#     elif event.chat_id not in auth_groups:
#         return
#     await event.reply("Hello!")


# @bot.on(events.NewMessage(pattern="/cancel"))
# async def _(event):
#     if event.is_private:
#         if event.sender_id not in auth_users:
#             return
#     elif event.chat_id not in auth_groups:
#         return
#     global cancel
#     cancel = True
#     await event.reply("Trying to cancel all processes.")
#     return


# @bot.on(events.NewMessage(pattern="/download"))
# async def _(event):
#     if event.is_private:
#         if event.sender_id not in auth_users:
#             return
#     elif event.chat_id not in auth_groups:
#         return
#     global cancel
#     cancel = False
#     try:
#         arg = int(event.raw_text.split(" ")[1])
#         arg -= 1
#     except:
#         arg = 0
#     try:
#         txt_file = await event.get_reply_message()
#         x = await bot.download_media(txt_file)
#         with open(x) as f:
#             content = f.read()
#         content = content.split("\n")
#         links = []
#         for i in content:
#             links.append(i.split(":", 1))
#         os.remove(x)
#     except:
#         await event.reply("Invalid file input.")
#         os.remove(x)
#         return
        
#     for i in range(arg, len(links)):
#         pass
          
          
@bot.on(events.NewMessage(pattern="/upload"))
async def _(event):
    # if event.is_private:
    #     if event.sender_id not in auth_users:
    #         return
    # elif event.chat_id not in auth_groups:
    #     return
    arg = event.raw_text.split(" ", maxsplit = 1)[1]
    arg = arg.split("|")
    if len(arg) == 1:
        file_name = helper.time_name()
        caption = None
    elif len(arg) == 2:
        file_name = arg[1].strip()
        caption = arg[1].strip()
    else:
        file_name = arg[1].strip()
        caption = arg[2].strip()

    cmd = f'yt-dlp -F "{arg[0]}"'
    k = await helper.run(cmd)
    out = helper.parse_vid_info(str(k))
    print(out)
    buttons = []
    for i in out:
        buttons.append([Button.inline(i[1], data=f"id:{i[0]}")])
    await bot.send_message(event.chat_id, f"`Name: {file_name}`\n`Caption: {caption}`\n`Url: {arg[0]}`", buttons=buttons)
    


# @bot.on(events.NewMessage(pattern="/txt"))
# async def _(event):
#     if event.is_private:
#         if event.sender_id not in auth_users:
#             return
#     elif event.chat_id not in auth_groups:
#         return
#     try:
#         x = await event.get_reply_message()
#         json_file = await bot.download_media(x)
#         res, count = helper.parse_json_to_txt(json_file)
#         await event.reply(f"{count} links detected." ,file=res)
#         os.remove(json_file)
#         os.remove(res)
#     except:
#         await event.reply("Invalid Json file input.")


# @bot.on(events.NewMessage(pattern="/html"))
# async def _(event):
#     if event.is_private:
#         if event.sender_id not in auth_users:
#             return
#     elif event.chat_id not in auth_groups:
#         return
#     try:
#         x = await event.get_reply_message()
#         json_file = await bot.download_media(x)
#         res, count = helper.parse_json_to_html(json_file)
#         await event.reply(f"{count} links detected." ,file=res)
#         os.remove(json_file)
#         os.remove(res)
#     except Exception:
#         await event.reply("Invalid Json file input.")


# @bot.on(events.CallbackQuery(pattern=b"id:"))
# async def _(event):
#     r = await event.reply("Trying to download....")
#     data = event.data.decode('utf-8')
#     data = data.split(":")
#     msg = await bot.get_messages(event.chat_id, ids=event.message_id)
#     msg = msg.raw_text.split("\n")
#     filename = msg[0].replace("Name: ", "")
#     caption = msg[1].replace("Caption: ", "")
#     url = msg[2].replace("Url: ", "") 
#     vid_id = (data[1])
#     k = await helper.download_video(url, filename, vid_id)
#     res_file = await fast_upload(bot, filename, r)
#     subprocess.call(f'ffmpeg -i "{filename}" -ss 00:00:01 -vframes 1 "{filename}.jpg"', shell=True)
#     dur = int(helper.duration(filename))
#     try:
#         await bot.send_message(
#             event.chat_id, 
#             f"`{caption}`", 
#             file=res_file, 
#             force_document=False, 
#             thumb=f"{filename}.jpg", 
#             supports_streaming=True, 
#             attributes=[DocumentAttributeVideo(
#                 duration=dur, 
#                 w=1260, 
#                 h=720, 
#                 supports_streaming=True
#             )]
#         )

#     except:
#         await bot.send_message(
#             event.chat_id,
#             "There was an error while uploading file as streamable so, now trying to upload as document."
#         )
#         await bot.send_message(
#             event.chat_id, 
#             f"`{caption}`", 
#             file=res_file, 
#             force_document=True,
#         )

#     os.remove(filename)
#     os.remove(f"{filename}.jpg")
#     await r.delete()   



bot.start()

bot.run_until_disconnected()

