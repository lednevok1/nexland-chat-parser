import requests as reqs
from re import sub

settings = {    # Настройки "бота"
                "nickname": "",
                "password": "",
                "server": "",
                "chatid": int(""),  # Только чаты
                "token": "",
                "doPrint": bool(1)  # 1 или 0
}
session = reqs.Session()

def createSession():  # Создаёт сессию на сайте, возвращает её ID
    session.get("https://nexland.fun/acc/login.php", params={"server": settings.get("server"), "name": settings.get("nickname"), "pass": settings.get("password")})
    reply = session.get("https://nexland.fun/acc/index.php").text
    x = reply.find("sessionId = '")
    sessionid = reply[x:x+60].split("'")[1]
    print(f"Session ID: {sessionid}\n")
    return sessionid

def listen(sessionid):  # Слушает сайт, возвращает последнее сообщение (разделяется через <br>)
    try:
        reply = session.get("https://nexland.fun/acc/api/api.php", params={"method": "get", "session": sessionid, "server": settings.get("server")}).text
    except:  # ну тут тоже какие-то маги наколдовали и лично у меня ошибки если у вас их не будет то уберёте
        reply = session.get("https://nexland.fun/acc/api/api.php", params={"method": "get", "session": sessionid, "server": settings.get("server")}).text
    return reply.split("<br>")[-1]

def main():
    lastmsg = None
    sessionid = createSession()
    while True:
        try:
            answer = listen(sessionid)
            if "not f" in answer:
                print("Session expired, generating another one...")
                sessionid = createSession()
                continue
            elif lastmsg == answer:
                continue
            lastmsg = answer
            if lastmsg.startswith("<span style=color:#5FF>[G]"):
                result = sub("<[^<]+?>", "", lastmsg)
                reqs.get("https://api.vk.com/method/messages.send", params={"v": 5.131, "peer_id": 2000000000 + settings.get("chatid"), "access_token": settings.get("token"), "random_id": 0, "message": result})
                if settings.get("doPrint"):
                    print(result)
        except:  # Оно постоянно кидает мне какие-то связанные с интернетом ошибки, поэтому ПРОСТО КИНЕМ ИХ В ИГНОР))
            continue

if __name__ == "__main__":
    main()
