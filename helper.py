import json
from config import skeleton_url
import subprocess

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
        link = f"https://thegreatace.herokuapp.com/{id}"
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
