import json
from config import skeleton_url
import subprocess
import datetime
import asyncio


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        return f'[stdout]\n{stdout.decode()}'
    if stderr:
        return f'[stderr]\n{stderr.decode()}'


def parse_json_to_txt(file_name):
    with open(file_name) as f:
        data = json.load(f)
    details = data["data"]["class_list"]["classes"]
    res = ""
    batch_name = data["data"]["class_list"]["batchName"]
    for i in details:
        name = i["lessonName"]
        id = i["lessonUrl"][0]["link"]
        link = f"{skeleton_url}/{id}"
        res = f"{name}:{link}\n{res}"
    new_file_name = f"{batch_name}.txt"
    with open(new_file_name, "w", encoding='utf-8') as f:
        f.write(res.strip())
    return (new_file_name, len(details))


def parse_json_to_html(file_name):
    with open(file_name) as f:
        data = json.load(f)
    batch_name = data["data"]["class_list"]["batchName"]
    details = data["data"]["class_list"]["classes"]
    for i in range( len(details) - 1, -1, -1):
        body_syntax = '''
        <p class="video">
            <span class="video_name">NAME</span>
            <br>
            <a href="LINK" class="youtube" rel="noopener noreferrer" target="_blank">LINK</a>
            </p>
        '''
        name = details[i]["lessonName"]
        id = details[i]["lessonUrl"][0]["link"]
        link = f"{skeleton_url}/{id}"
        body_syntax = body_syntax.replace("NAME", name)
        body_syntax = body_syntax.replace("LINK", link)
        with open(f"{batch_name}.html", "a", encoding='utf-8') as f:
            f.write(body_syntax)
    return (f"{batch_name}.html", len(details))
    

def duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)


def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"


def time_name():
    date = datetime.date.today()
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M%S")
    return f"{date} {current_time}.mp4"


def parse_vid_info(info):
    info = info.strip()
    info = info.split("\n")
    new_info = []
    for i in info:
        i = str(i)
        if "[" not in i and '-' not in i:
            while "  " in i:
                i = i.replace("  ", " ")
            i.strip()
            i = i.split("|")[0].split(" ",2)
            try:
                if "RESOLUTION" not in i[2]:
                    new_info.append((i[0], i[2]))
            except:
                pass
    return new_info


async def download_video(url, name, ytf):
    cmd = f'yt-dlp -o "{name}" -f {ytf} "{url}"'
    k = await run(cmd)
    return k

