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
    return new_file_name


def parse_json_to_html(file_name):
    head_syntax = '''
    <!doctype html>
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <title>BATCH</title>

            <style>
                .note, .video{
                    text-align: center;
                    font-size: 20px;
                }
                .topic_button{
                background-color: #777;
                color: white;
                cursor: pointer;
                padding: 18px;
                width: 100%;
                border: none;
                text-align: center;
                outline: none;
                font-size: 35px;
                }

                .active, .topic_button:hover {
                background-color: #555;
                }

                .topic_content {
                padding: 0 18px;
                display: none;
                overflow: hidden;
                text-align:center;
                background-color: #f1f1f1;
                }
            </style>
        </head>
        <body>
            <h1 id="batch" style="text-align:center;font-size:50px;color:Red">
                Maths Spl-28 (Ari+Adv.)
            </h1>
            <p id="info" style="text-align:center;font-size:25px;color:Blue">
            Links grabber made by <a href="https://t.me/Portgas_D_ACEx" rel="noopener noreferrer" target="_blank">Scorpions Bot</a>
            <br>
            <br>
            </p>
    <div id="videos" class="files"> 
    '''
    with open(file_name) as f:
        data = json.load(f)
    batch_name = data["data"]["class_list"]["batchName"]
    head_syntax = head_syntax.replace("BATCH", batch_name)
    details = data["data"]["class_list"]["classes"]
    with open(f"{batch_name}.html", "w") as f:
        f.write(head_syntax)
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
    return f"{batch_name}.html"
    

def duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)
