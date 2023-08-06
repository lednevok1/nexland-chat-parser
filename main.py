import requests as reqs
from re import sub
from time import time, sleep

code = int(time() * 1000)
options = {
    "name": "456", "password": "123", 
    "server": "",  # 1, 2, 3, 4, 5, 6, 7, 8, sw, sw2
    
    "chatid": int("7"), 
    "token": "8",
    
    "print": True,  # True/False (с заглав. буквы)
    "debug": False
}
headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'Connection': 'keep-alive', 'Cookie': 'PHPSESSID=094kf4in2mrejt2r1hgaq3epcn', 'Host': 'nexland.fun', 'Referer': 'https://nexland.fun/acc/index.php', 'sec-ch-ua': '"Not:A-Brand";v="99", "Chromium";v="112"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 3a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'}
session = reqs.Session();

def newSession():
    if options.get("debug"):    print("called function: newSession")
    session.get("https://nexland.fun/acc/login.php", headers=headers, params={"server": options.get("server"), "name": options.get("name"), "pass": options.get("password"), "_": str(int(time()*1000))})
    response = session.get("https://nexland.fun/acc/index.php", headers=headers).text
    index = response.find("const sessionId = '")
    sessionid = response[index:index+60].split("'", maxsplit=2)[1]
    
    print("new sessionid:", sessionid)
    return sessionid

def parse(sessionid):
    if options.get("debug"):    print("called function: parse with sessionid:", sessionid)
    global code
    try:
        response = session.get("https://nexland.fun/acc/api/api.php", headers=headers, params={"method": "get", "session": sessionid, "server": str(options.get("server")), "_": code}).text
    except:
        response = session.get("https://nexland.fun/acc/api/api.php", headers=headers, params={"method": "get", "session": sessionid, "server": str(options.get("server")), "_": int(time()*1000)}).text
    code = code + 1
    if options.get("debug"):    print("newSession returned:", response.split("<br>")[-1])
    return response.split("<br>")[-1]

def beautify(text):
    if options.get("debug"):    print("called function: beautify")
    result = sub("<[^<]+?>", "", text)
    result = result.replace("@", "@;").replace("*", "*;")
    if options.get("debug"):    print("beautify returned:", result)
    return result

def main():
    sessionid = newSession()
    lastmessage = ""
    sleep(4)
    while True:
        print("iter started")
        start = int(time() * 1000)
        try:    message = beautify(parse(sessionid))
        except Exception as exc:
            print(f"ERROR [{exc}], RETRYING")
            message = beautify(parse(sessionid))
        
        if message == lastmessage or message == "chat.type.text" or message == "Session not found":
            print("ту би кантинуед")
            if message == "Session not found":
                sessionid = newSession()
            end = int(time()*1000)
            sleeptime = (1000 - (end - start)) / 1000
            if sleeptime < 0:    sleeptime = 0
            sleep(sleeptime)
            continue
        if message == "Доступ запрещен":
            print("\"Доступ запрещен\" detected, termintating process..."); return 1
        
        lastmessage = message
        if options.get("print"):    print(message)
        try:    reqs.get(f"https://api.telegram.org/bot{options.get('token')}/sendMessage", params={"chat_id": options.get("chatid"), "text": message, "parse_mode": "html"})
        except Exception as exc:
            print(f"ERROR [{exc}], RETRYING")
            reqs.get(f"https://api.telegram.org/bot{options.get('token')}/sendMessage", params={"chat_id": options.get("chatid"), "text": message, "parse_mode": "html"})
        end = int(time()*1000)
        sleeptime = (1000 - (end - start)) / 1000
        if sleeptime < 0:    sleeptime = 0
        print("sleeping", sleeptime)
        sleep(sleeptime)

main()
