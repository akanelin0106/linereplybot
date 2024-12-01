# -*- coding: utf-8 -*-
from CHRLINE import*
import time,sys,os,datetime
import json,codecs
import random,ast,pytz # type: ignore
import threading,io,re
from threading import Thread
from contextlib import redirect_stdout
import base64,hashlib,hmac,subprocess
from TaiwanLottery import TaiwanLotteryCrawler # type: ignore
from pt import *
import shutil
import instaloader # type: ignore
import uuid,requests
#File: bot.py
ALLIDS_REGEX= re.compile(r'(?<![a-f0-9])[ucr][a-f0-9]{32}(?![a-f0-9])')
cities = ["嘉義縣", "新北市", "嘉義市", "新竹縣", "新竹市", "臺北市", "臺南市", "宜蘭縣", "苗栗縣", "雲林縣", "花蓮縣", "臺中市", "臺東縣", "桃園市", "南投縣", "高雄市", "金門縣", "屏東縣", "基隆市", "澎湖縣", "彰化縣", "連江縣"]
########################################################Login
cl = CHRLINE(
    "u07fc84cf45da11205e216f7d12aed362:aWF0OiAxMDM2NTEzODkzNjAK..4qVydi+Su22gfNrjVVshHnVcafA=",
    device="IOS",
    useThrift=True
    )#Login
########################################################Login
read = {
    'readed':{},
    'readed2':{},
    'backread':{},
}
msg_dict={}
image_dict={}
video_dict={}
audio_dict={}
sticker_dict={}
contact_dict={}
file_dict={}
##########################################################ig download def
def download_instagram_videos(to, url):
    # 建立 Instaloader 物件
    L = instaloader.Instaloader()

    # 從 URL 提取短碼 (shortcode)
    shortcode_match = re.search(r'/p/([A-Za-z0-9_-]+)/|/reel/([A-Za-z0-9_-]+)/', url)
    if not shortcode_match:
        return "無法從 URL 提取短碼，請檢查 URL 是否正確。"

    shortcode = shortcode_match.group(1) or shortcode_match.group(2)

    try:
        # 提取貼文內容
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # 動態生成目錄名稱（使用時間戳）
        download_dir = f"downloads_{time.strftime('%Y%m%d_%H%M%S')}"
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # 下載貼文內容
        L.download_post(post, target=download_dir)

        # 篩選影片檔案
        downloaded_files = []
        for file in os.listdir(download_dir):
            file_path = os.path.join(download_dir, file)
            if file.endswith('.mp4'):  # 篩選影片
                # 重新命名檔案，確保唯一性
                unique_filename = f"{time.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.mp4"
                new_path = os.path.join(download_dir, unique_filename)

                os.rename(file_path, new_path)

                # 傳送影片
                try:
                    cl.sendVideo(to, new_path)  # 使用 sendVideo 發送影片
                    downloaded_files.append(new_path)
                    os.remove(new_path)
                except Exception as send_error:
                    print(f"傳送影片失敗：{new_path}，錯誤：{send_error}")

        if not downloaded_files:
            return "未找到任何影片檔案，請確認貼文是否包含影片。"
        shutil.rmtree(download_dir)
        return downloaded_files

    except Exception as e:
        return f"下載失敗：{str(e)}"
def download_instagram_images(to, url):
    # 建立 Instaloader 物件
    L = instaloader.Instaloader()

    # 從 URL 提取短碼 (shortcode)
    shortcode_match = re.search(r'/p/([A-Za-z0-9_-]+)/|/reel/([A-Za-z0-9_-]+)/', url)
    if not shortcode_match:
        return "無法從 URL 提取短碼，請檢查 URL 是否正確。"

    shortcode = shortcode_match.group(1) or shortcode_match.group(2)

    try:
        # 提取貼文內容
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # 動態生成目錄名稱（使用時間戳）
        download_dir = f"downloads_{time.strftime('%Y%m%d_%H%M%S')}"
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # 下載貼文內容
        L.download_post(post, target=download_dir)

        # 篩選圖片檔案
        downloaded_files = []
        for file in os.listdir(download_dir):
            file_path = os.path.join(download_dir, file)
            if file.endswith(('.jpg', '.jpeg', '.png')):  # 篩選圖片
                # 重新命名檔案，確保唯一性
                unique_filename = f"{time.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}{os.path.splitext(file)[1]}"
                new_path = os.path.join(download_dir, unique_filename)

                os.rename(file_path, new_path)

                # 傳送圖片
                try:
                    cl.sendImage(to, new_path)  # 發送完整檔案路徑
                    downloaded_files.append(new_path)
                    os.remove(new_path)
                except Exception as send_error:
                    print(f"傳送檔案失敗：{new_path}，錯誤：{send_error}")

        if not downloaded_files:
            return "未找到任何圖片檔案，請確認貼文是否包含圖片。"
        shutil.rmtree(download_dir)
        return downloaded_files

    except Exception as e:
        return f"下載失敗：{str(e)}"
##########################################################ig download def
def get_taiwan_time():
    # 設定台灣時區
    tz = pytz.timezone('Asia/Taipei')
    # 取得當前時間並轉換為台灣時區
    taiwan_time = datetime.datetime.now(tz)
    # 格式化時間
    return taiwan_time.strftime('(%H:%M)')

########################################################name update
bot_name = "企鵝回復機"
try:
    cl.updateProfileAttribute(2, f"{(bot_name).split()[0]} {get_taiwan_time()}")
except:pass
def nameUpdate():
    try:
       cl.updateProfileAttribute(
                    2, f"{(bot_name).split()[0]} {get_taiwan_time()}")
    except:pass
def schedule():
    while True:
        now = datetime.datetime.now()
        if now.minute % 5 == 0 and now.second == 0:
            nameUpdate()
            time.sleep(1)
        else:time.sleep(0)
########################################################name update
threading.Thread(target=schedule).start()
def login():
    subprocess.run(["python3", "qrbot.py"])
#2024-08-22 09:55
fkubao=[]
daily_horoscope=json.load(codecs.open("Json/fort.json","r","utf-8"))
settings=json.load(codecs.open("Json/settings.json","r","utf-8"))
signin = json.loads(open('Json/signin.json','r',encoding="utf-8").read())
admin = settings['admin']
status=settings["status"]
backdoor = "c80fee1ca10e8a7b7dc27ebbb5c95dcd2"
startTime = time.time()
#
user_timestamps = {}


# 定义消息发送限制（例如 10 秒内不允许发送超过 3 条消息）
TIME_WINDOW = 10  # 秒
MAX_MESSAGES = 3  # 在时间窗口内允许的最大消息数

def is_spamming(sender):
    current_time = time.time()
    if sender not in user_timestamps:
        user_timestamps[sender] = []
    
    # 过滤掉时间窗口外的消息时间戳
    user_timestamps[sender] = [timestamp for timestamp in user_timestamps[sender] if current_time - timestamp <= TIME_WINDOW]

    # 如果在时间窗口内的消息数超过限制，判断为刷屏
    if len(user_timestamps[sender]) >= MAX_MESSAGES:
        return True
    
    # 否则，记录这次消息的时间戳
    user_timestamps[sender].append(current_time)
    return False

choices = ["石頭", "剪刀", "布"]
user_scores = settings['user_scores']
# 猜拳遊戲函數
def update_score(mid, result):
    if mid not in user_scores:
        # 如果用戶尚無分數紀錄，初始化
        user_scores[mid] = {"win": 0, "lose": 0, "draw": 0}
    # 根據結果更新分數
    if result == "win":
        user_scores[mid]["win"] += 1
    elif result == "lose":
        user_scores[mid]["lose"] += 1
    elif result == "draw":
        user_scores[mid]["draw"] += 1
def play_rps(mid,user_choice):
    # 機器人隨機選擇
    bot_choice = random.choice(choices)

    # 判定勝負
    if user_choice == bot_choice:
        result = "平手！"
        update_score(mid, "draw")
    elif (user_choice == "石頭" and bot_choice == "剪刀") or \
         (user_choice == "剪刀" and bot_choice == "布") or \
         (user_choice == "布" and bot_choice == "石頭"):
        result = "你贏了！"
        update_score(mid, "win")
    else:
        result = "你輸了！"
        update_score(mid, "lose")
    # 回傳結果
    flex_message666 = {
    "type": "flex",
    "altText": "遊戲結果",
    "contents": {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "遊戲結果",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "你選擇了",
                                    "color": "#111111",
                                    "size": "md",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": user_choice,
                                    "color": "#111111",
                                    "size": "md",
                                    "align": "end",
                                    "flex": 1
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "機器人選擇了",
                                    "color": "#111111",
                                    "size": "md",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": bot_choice,
                                    "color": "#111111",
                                    "size": "md",
                                    "align": "end",
                                    "flex": 1
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "結果",
                                    "color": "#111111",
                                    "size": "md",
                                    "flex": 2
                                },
                                {
                                    "type": "text",
                                    "text": result,
                                    "color": "#111111",
                                    "size": "md",
                                    "align": "end",
                                    "flex": 1
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }
}

    return flex_message666
game_state = {
    "active": False,
    "target_number": None,
    "attempts": 0
}
def start_game():
    game_state["active"] = True
    game_state["target_number"] = random.randint(1, 100)
    game_state["attempts"] = 0
    return "游戏开始！我已经选好了1到100之间的一个数字，来猜猜看吧！"
###########################
def handle_guess(guess):
    if not game_state["active"]:
        return "游戏尚未开始，请输入 '开始' 来启动游戏。"

    try:
        guess = int(guess)
    except ValueError:
        return "请输入一个有效的数字。"

    game_state["attempts"] += 1

    if guess < game_state["target_number"]:
        return "猜小了，再试试吧！"
    elif guess > game_state["target_number"]:
        return "猜大了，再试一次！"
    else:
        game_state["active"] = False
        return f"恭喜你，猜对了！你一共猜了 {game_state['attempts']} 次。输入 '開始' 重新开始游戏。"
customer_complaint_event = {"name": "奧客投訴", "effect": "心情下降 30 點"}
events = [
    {"name": "周邊", "effect": "借高利貸[獲得欠債狀態], 資產上升, 心情上升"},
    {"name": "心趴", "effect": "心情上升"},
    {"name": "旅遊大亨", "effect": "資產下降, 心情上升"},
    {"name": "社區活動", "effect": "被規制[獲得禁言狀態], 心情下降"},
    {"name": "炸薯條", "effect": "資金上升, 心情上升"},
    {"name": "爆米花", "effect": "資產上升（比炸薯條多）, 心情下降"},
    {"name": "小帝出現", "effect": "資產下降, 心情下降"},
    {"name": "西瓜出現", "effect": "心情上升"},
    {"name": "社區價值", "effect": "向日本屈服[獲得跪舔狀態], 心情上升"},
    {"name": "辭職", "effect": "心情下降 40, 十回合內不會出現炸薯條或爆米花"}
]
disable_fries_or_popcorn = 0
trigger_complaint = False
disable_heart_sleep = 0  # 用於禁用“心趴”的回合數

# 定義負面事件

negative_events = [
    {"name": "社區活動", "effect": "被規制[獲得禁言狀態], 心情下降"},
    {"name": "小帝出現", "effect": "資產下降, 心情下降"}
]

def handle_event(msg,event):
    if event.get("forced"):
        status["資產"] -= 10
        if event.get("name") == "清洗":
            disable_heart_sleep = 5
        cl.replyMessage(msg,f"強制事件：{event['name']}，效果：{event['effect']}")
    else:
        update_status(msg,event)

# 隨機選擇事件
def choose_event():
    global status
    if status["禁言"]:
        # 禁言狀態下負面事件的機率增加
        if random.randint(1, 3) == 1:
            return random.choice(negative_events)
    
    # 選擇一個隨機事件
    event = random.choice(events)
    
    # 禁用 "炸薯條" 或 "爆米花" 的邏輯
    if disable_fries_or_popcorn > 0 and event["name"] in ["炸薯條", "爆米花"]:
        event = random.choice([e for e in events if e["name"] not in ["炸薯條", "爆米花"]])
    elif disable_heart_sleep > 0 and event["name"] == "心趴":
        event = random.choice([e for e in events if e["name"] != "心趴"])
    
    return event

# 明夫歷險記的事件觸發函數
def play_adventure(msg, to):
    global trigger_complaint, disable_fries_or_popcorn, disable_heart_sleep
    
    if trigger_complaint:
        event = customer_complaint_event
        trigger_complaint = False
    else:
        event = choose_event()
        
        if disable_heart_sleep > 0:
            if event["name"] == "心趴":
                event = random.choice([e for e in events if e["name"] != "心趴"])
            disable_heart_sleep -= 1
        
        # 檢查是否觸發 "奧客投訴"
        if event["name"] in ["炸薯條", "爆米花"] and random.randint(1, 20) == 1:
            trigger_complaint = True
        
    print(f"事件：{event['name']}")
    print(f"效果：{event['effect']}")
    handle_event(msg, event)

    flex_message2222 = {
        "type": "flex",
        "altText": "事件效果",
        "contents": {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "事件",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center"
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "名稱",
                                        "color": "#111111",
                                        "size": "md",
                                        "flex": 2,
                                        "wrap": True  # 允許名稱換行
                                    },
                                    {
                                        "type": "text",
                                        "text": event['name'],
                                        "color": "#111111",
                                        "size": "md",
                                        "align": "end",
                                        "flex": 3,
                                        "wrap": True  # 允許名稱換行
                                    }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "效果",
                                        "color": "#111111",
                                        "size": "md",
                                        "flex": 2,
                                        "wrap": True  # 允許效果換行
                                    },
                                    {
                                        "type": "text",
                                        "text": event['effect'],
                                        "color": "#111111",
                                        "size": "md",
                                        "align": "end",
                                        "flex": 3,
                                        "wrap": True  # 允許效果換行
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    }
    cl.sendLiff(to, flex_message2222)

    # 回覆訊息給用戶
    #cl.replyMessage(msg, f"事件：{event['name']}\n效果：{event['effect']}")

def update_status(msg,event):
    global status, trigger_complaint, disable_fries_or_popcorn, disable_heart_sleep
    if event["name"] == "周邊":
        status["欠債"] += 1
        status["資產"] += 10
        status["心情"] += 10
    elif event["name"] == "心趴":
        status["心情"] += 10
        status["心趴計數"] += 1
        if status["心趴計數"] % 5 == 0:
            # 強制事件“清洗”
            handle_event(msg,({"name": "清洗", "effect": "資產下降, 五回合內不會再出現“心趴”選項", "forced": True}))
    elif event["name"] == "旅遊大亨":
        status["資產"] -= 20
        status["心情"] += 5
    elif event["name"] == "社區活動":
        status["禁言"] = True
        status["心情"] -= 10
    elif event["name"] == "炸薯條":
        status["資金"] += 15
        status["心情"] += 10
        status["健康"] -= 10  # 工作類事件，健康下降
    elif event["name"] == "爆米花":
        status["資產"] += 25
        status["心情"] -= 10
        status["健康"] -= 10  # 工作類事件，健康下降
    elif event["name"] == "小帝出現":
        status["資產"] -= 15
        status["心情"] -= 10
    elif event["name"] == "西瓜出現":
        status["心情"] += 10
        status["健康"] = min(status["健康"] + 20, 100)  # 健康值上限為100
    elif event["name"] == "社區價值":
        status["跪舔"] = True
        status["心情"] += 5
    elif event["name"] == "辭職":
        status["心情"] -= 40
        disable_fries_or_popcorn = 10  # 禁用 10 回合內的 "炸薯條" 和 "爆米花"
    elif event["name"] == "賣腎":
        # 用健康值來轉換資產
        conversion_amount = min(50, status["健康"])
        status["資產"] += conversion_amount
        status["健康"] -= conversion_amount
        if status["健康"] <= 0:
            handle_death()
    elif event["name"] == "便利店食品":
        status["資產"] -= 5
        if status["健康"] < 50:
            status["健康"] = min(status["健康"] + 20, 100)  # 健康值回復，最大值為100
        elif status["健康"] > 60:
            status["健康"] -= 5
    elif event["name"] == "賣手機":
        if status["欠債"] > 0:
            status["欠債"] -= 1
        status["資產"] += 20
        cl.replyMessage(msg,"獲得成就：[賣手機]")
    elif event["name"] == "社區戰績":
        if status["禁言"]:
            cl.replyMessage(msg,"無法出現戰績選項，請先解除禁言狀態。")
        else:
            status["心情"] += 15
            status["健康"] = min(status["健康"] + 10, 100)
            # 增加社區活動和社區價值選項的機率
            # 這裡可以增加機率修改邏輯

    # 檢查是否需要解除欠債
    if status["資產"] >= 50:
        status["資產"] -= 50
        status["欠債"] = 0
    
    # 欠債狀態自動增長
    if status["欠債"] > 0 and status["事件計數"] % 5 == 0:
        status["欠債"] += 1

    # 欠債狀態到達 10 層，小明夫死亡
    if status["欠債"] >= 10:
        handle_death(msg)
    
    # 每三個事件視為過了一天
    status["事件計數"] += 1
    if status["事件計數"] == 3:
        status["天數"] += 1
        status["事件計數"] = 0

    # 健康降到 0，表示小明夫死亡
    if status["健康"] <= 0:
        handle_death(msg)
def reset_status():
    global status  # 宣告 status 是全局變數
    status["資產"] = 100
    status["資金"] = 50
    status["心情"] = 50
    status["健康"] = 100
    status["天數"] = 0
    status["事件計數"] = 0
    status["欠債"] = 0
    status["心趴計數"] = 0
    status["禁言"] = False
    status["跪舔"] = False
# 處理死亡邏輯
# 更新狀態
def handle_death(msg):
    cl.replyMessage(msg,f"小明夫死亡！他活了 {status['天數']} 天。"+f"\n臨死前狀態：資產: {status['資產']}, 資金: {status['資金']}, 心情: {status['心情']}, 健康: {status['健康']}"+f"\n死亡原因：健康耗盡" if status["健康"] <= 0 else "死亡原因：欠債過多")
    #cl.replyMessage(msg,f"死亡原因：健康耗盡" if status["健康"] <= 0 else "死亡原因：欠債過多")
    #cl.replyMessage(msg,f"臨死前狀態：資產: {status['資產']}, 資金: {status['資金']}, 心情: {status['心情']}, 健康: {status['健康']}")
    # 根據狀態解鎖成就
    achievements = []
    if status["欠債"] > 0:
        achievements.append("債務纏身")
    if status["禁言"]:
        achievements.append("社區之王")
    if status["跪舔"]:
        achievements.append("屈服之心")
    
    if achievements:
        cl.replyMessage(msg,f"解鎖成就：{', '.join(achievements)}")
    else:
        cl.replyMessage(msg,"沒有解鎖任何成就。")
    reset_status()


tarot_readings = [
    "愚者：勇氣和新開始的象徵，今天是冒險的好時機。",
    "魔術師：創造力和行動力的象徵，抓住機會實現目標。",
    "女祭司：直覺和內在智慧的象徵，信任你的感覺。",
    "皇后：豐饒和創造的象徵，關注家庭和生活的美好。",
    "皇帝：權威和穩定的象徵，今天需要採取領導角色。",
    "教皇：傳統和智慧的象徵，尋求指導和支持。",
    "戀人：愛情和和諧的象徵，關注重要的關係和選擇。",
    "戰車：勝利和決心的象徵，克服障礙取得成功。",
    "力量：內心力量和勇氣的象徵，信任自己。",
    "隱者：內省和指導的象徵，尋找內心的智慧。",
    "命運之輪：命運和變化的象徵，保持開放的心態。",
    "正義：公平和真相的象徵，追求真理。",
    "倒吊人：犧牲和放棄的象徵，重新評估現狀。",
    "死亡：結束和新開始的象徵，迎接變化。",
    "節制：平衡和調和的象徵，保持冷靜。",
    "惡魔：誘惑和束縛的象徵，警惕潛在的誘惑。",
    "塔：突發的變化和啟示，重新審視生活。",
    "星星：希望和靈感的象徵，保持積極的心態。",
    "月亮：潛意識和幻覺的象徵，依賴直覺。",
    "太陽：快樂和成功的象徵，享受美好的一天。",
    "審判：反思和重生的象徵，是時候審視選擇。",
    "世界：完成和成就的象徵，享受達成目標的喜悅。"
]

def draw_lucky_penguin():
    penguins = [
        "皇帝企鵝",
        "黃眼企鵝",
        "馬卡羅尼企鵝（長冠企鵝）",
        "阿德利企鵝",
        "峽灣企鵝（毛利企鵝、鳳冠企鵝、福德蘭企鵝）",
        "巴布亞企鵝（紳士企鵝、金圖企鵝）",
        "國王企鵝",
        "皇家企鵝",
        "冠毛企鵝（豎毛企鵝）",
        "漢波德企鵝（洪堡企鵝）",
        "跳岩企鵝",
        "白鰭企鵝",
        "南極企鵝（頰帶企鵝、帽帶企鵝、鬍鬚企鵝）",
        "麥哲倫企鵝",
        "黑腳企鵝（非洲企鵝、斑嘴環企鵝）",
        "史納爾島企鵝（黃眉企鵝）",
        "加拉帕戈斯企鵝",
        "小藍企鵝（神仙企鵝）"
    ]
    
    # 隨機選擇一隻幸運企鵝
    lucky_penguin = random.choice(penguins)
    
    return lucky_penguin
def draw_lucky_penguin2():
    penguins = [
        "馬達加斯加 爆走企鵝",
        "豬血糕爆氣企鵝",
        "跳樓企鵝",
        "上吊企鵝",
        "殭屍企鵝",
        "飢餓三十企鵝",
        "皮包骨企鵝",
        "躺分企鵝",
        "送頭企鵝",
        "自慰企鵝",
        "野外露出企鵝",
        "倉鼠企鵝"
    ]
    
    # 隨機選擇一隻幸運企鵝
    lucky_penguin = random.choice(penguins)
    
    return lucky_penguin
# 抽取幸運企鵝
try:
    print(cl.registerE2EESelfKey())
except:
    print(cl.registerE2EESelfKey())
###########################
wait = {
    'changePictureProfile':{},
    'changeCoverProfile': {},
    'changeChatJoinPicture':{},
    'changeChatLeavePicture':{},
    "penguin":{},
    "bc":{},
    'akane': False,
    'akane2': False,
    'xin':"",
}
def Save():
    try:
        json.dump(settings, codecs.open('Json/settings.json', 'w', 'utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
        with open('Json/signin.json', 'w',encoding='utf-8') as fp:json.dump(signin, fp, sort_keys=True, indent=4, ensure_ascii=False)
        return f"Save"
    except:
        return f"Not Save"
def save_flex(to):
    penguin_image_url = "https://plus.unsplash.com/premium_photo-1661816797370-928a8749043c?q=80&w=1773&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    flex_message = {
        "type": "flex",
        "altText": "速度測試結果",
        "contents": {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": penguin_image_url,
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "儲存",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#000000"
                    },
                    {
                        "type": "text",
                        "text": f"成功儲存",
                        "size": "md",
                        "color": "#1E90FF",
                        "margin": "md"
                    }
                ]
            }
        }
    }
    cl.sendLiff(to,flex_message)
def speed_test_flex(to):
    t1 = time.time()
    cl.sendMessage(to, '速度測試中...')
    t2 = time.time() - t1

    # 企鹅图片的 URL
    penguin_image_url = "https://images.unsplash.com/photo-1680371431292-22e95260c8e4?q=80&w=1899&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"

    # 构建 Flex Message
    flex_message = {
        "type": "flex",
        "altText": "速度測試結果",
        "contents": {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": penguin_image_url,
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "速度測試結果",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#000000"
                    },
                    {
                        "type": "text",
                        "text": f"速度：{t2:.2f} 秒",
                        "size": "md",
                        "color": "#1E90FF",
                        "margin": "md"
                    }
                ]
            }
        }
    }
    cl.sendLiff(to,flex_message)
# 调用函数进行速度测试并发送 Flex Message


def botruntime_flex():
    # 计算机器人的运行时间
    elapsed_time = datetime.timedelta(seconds=int(time.time() - startTime))
    days, seconds = divmod(elapsed_time.total_seconds(), 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    # 企鹅图片的 URL
    penguin_image_url = "https://i.imgur.com/8KxGULQ.jpeg"

    # 构建 Flex Message
    flex_message = {
        "type": "flex",
        "altText": "機器人運行時間",
        "contents": {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": penguin_image_url,
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "機器人運行時間",
                        "weight": "bold",
                        "size": "lg",
                        "color": "#000000"
                    },
                    {
                        "type": "text",
                        "text": '登入時間: %02d天 %02d小時 %02d分 %02d秒' % (days, hours, minutes, seconds),
                        "size": "md",
                        "color": "#1E90FF",
                        "margin": "md"
                    }
                ]
            }
        }
    }
    
    return flex_message

def generate_slots():
    slots = []
    for _ in range(5):
        row = [random.randint(1, 9) for _ in range(3)]
        slots.append(row)
    return slots
def check_winner(slots):
    for i, row in enumerate(slots):
        if row[0] == row[1] == row[2]:
            return i + 1
    return None

def restart_program():
    Save()
    python = sys.executable
    os.execl(python, python, * sys.argv)

def bot(op,cl:CHRLINE):
    if op.type == 0:
        return
    elif op.type == 5:
        return
    elif op.type == 30:
        update_type = op.param3
        if update_type == "c":
            a = cl.getChatRoomAnnouncements(op.param1)[0]
            creator = a.creatorMid
            ret = (
                f"[公告已被創建]\n"
                f"創建者:@!\n"
                f"文字: {a.contents.text}"
                #f"連結: {a.contents.link}"
            )
            cl.sendMention(op.param1,ret,creator)
    elif op.type == 55:
        if op.param1 in read["readed"]:
            if op.param2 not in read["readed"][op.param1]:
                read["readed"][op.param1].append(op.param2)
                cl.sendMention(op.param1,"@! 抓到你已讀了",op.param2)
            else:...
        elif op.param1 in read["readed2"]:
            if op.param2 not in read["readed2"][op.param1]:
                created_time = op.createdTime
                read["readed2"][op.param1].append((op.param2, created_time))
                read['backread'][op.param1] += f"\n{cl.getContact(op.param2).displayName}"
            else:
                ...  
    elif op.type == 26:
        try:
            global msgType
            msg = op.message
            text = msg.text
            to = msg.to
            sender = msg._from
            msg_id = msg.id
            cmd = text.lower()
        except:cmd = None;text = None
        if msg.contentType == 0:
            if msg.toType == 2 or msg.toType == 0:
                if msg.contentMetadata is not None and 'e2eeVersion' in msg.contentMetadata:
                    try:
                        text = cl.decryptE2EETextMessage(msg,isSelf=False)
                        sender = msg._from
                        msg_id = msg.id
                        to = msg.to
                        cmd = text.lower()
                    except Exception as e:pass

                if msg.contentMetadata is not None and 'MENTION' in msg.contentMetadata:
                    mentions = eval(msg.contentMetadata["MENTION"])["MENTIONEES"]
                    for mention in mentions:
                        user_id = mention["M"]
                        tag_file = f"tag/{user_id}.json"
                        if os.path.isfile(tag_file):
                            with codecs.open(tag_file, "r", "utf-8") as f:
                                who_mark_me = json.load(f)
                        else:
                            who_mark_me = {}
                        if to not in who_mark_me: who_mark_me[to] = {}
                        tag_num = len(who_mark_me[to]) + 1
                        who_mark_me[to][str(tag_num)] = {
                            "sender": sender,
                            "msgid": msg_id,
                            "tagtime": datetime.datetime.now(pytz.timezone("Asia/Taipei")).strftime('%m/%d %H:%M:%S')
                        }
                        with codecs.open(tag_file, "w", "utf-8") as f:
                            json.dump(who_mark_me, f, sort_keys=True, indent=4, ensure_ascii=False)
                if sender in admin or to in settings['chatadmin'] and sender in settings['chatadmin'][to]:
                    if cmd == "sp":
                        speed_test_flex(to)
                    if cmd == "save":
                        Save()
                        save_flex(to)
##################################################################################ig下載
                    if cmd.startswith("igp:"):
                        try:
                            txt = text[4:]
                            cl.sendMessage(to,'嘗試下載ig照片')
                            #download_instagram_content(txt,image)
                            download_instagram_images(to,txt)
                        except Exception as e:
                            cl.sendMessage(to,str(e))
                    if cmd.startswith("igv:"):
                        try:
                            txt = text[4:]
                            cl.sendMessage(to,'嘗試下載ig影片')
                            #download_instagram_content(txt,image)
                            download_instagram_videos(to,txt)
                        except Exception as e:
                            cl.sendMessage(to,str(e))
##################################################################################ig下載
                    elif text is not None and text.startswith("設定進群:"):
                        try:
                            txt = text[5:]
                            settings['welcome'][to] = txt
                            if "@!" in txt:
                                cl.sendMention(to,f"設定成功\n預覽:\n{txt}",[sender])
                            else:
                                cl.sendMessage(to,f"設定成功\n預覽:\n{txt}")
                            Save()
                        except Exception as e:
                            cl.sendMessage(to,str(e))
                    elif text is not None and text.startswith("設定退群:"):
                        try:
                            txt = text[5:]
                            settings['leave'][to] = txt
                            if "@!" in txt:
                                cl.sendMention(to,f"設定成功\n預覽:\n{txt}",[sender])
                            else:
                                cl.sendMessage(to,f"設定成功\n預覽:\n{txt}")
                            Save()
                        except Exception as e:
                            cl.sendMessage(to,str(e))
                    elif cmd == "設定進群圖片":
                        wait["changeChatJoinPicture"][sender] = True
                        cl.sendMessage(to, "請傳送圖片")
                        return
                    elif cmd == "設定退群圖片":
                        wait["changeChatLeavePicture"][sender] = True
                        cl.sendMessage(to, "請傳送圖片")
                        return
##################################################################################歡迎基本
                    elif cmd == "bye":
                        cl.deleteSelfFromChat(to)
                if sender in admin:
                    if cmd =="公告":
                        abcde=cl.getChatRoomAnnouncements(to)
                        cl.sendMessage(to,abcde)
                    elif cmd.startswith("加公告"):
                        x = text.split(' ')
                        link="line://nv/chatMsg?chatId={}&messageId={}".format(to,msg_id)
                        cl.createChatRoomAnnouncement(to,x[1],link)
                        cl.sendMessage(to,"成功")
                    elif cmd == "e2ee":
                        try:
                            cl.getE2EESelfKeyData()
                            cl.sendMessage(to, "e2ee succes")
                        except:
                            cl.registerE2EESelfKey()
                            cl.sendMessage(to, "e2ee succes")
                    elif cmd == "reboot":
                        cl.sendMessage(to,"重啟中...")
                        settings["reboot"]=to
                        restart_program()
                    elif cmd == "查詢已讀":
                        if to in read["readed2"]:
                            current_time = int(time.time())
                            backread_text = "[已讀點查詢]"
                            shown_users = set()
                            n = 0
                            for user_id, created_time in read["readed2"][to]:
                                if user_id not in shown_users:
                                    time_diff = current_time - created_time / 1000
                                    minutes = int(time_diff // 60)
                                    seconds = int(time_diff % 60)
                                    n+=1
                                    backread_text += f"\n[{n}]. {cl.getContact(user_id).displayName}\n已讀時間:{minutes}分{seconds}秒前已讀"
                                    shown_users.add(user_id)
                            cl.sendMessage(to, backread_text)
                        else:cl.sendMessage(to, "沒有設置已讀點")
##################################################################################回復
                    elif cmd.startswith("關鍵 "):
                        x = text.split(' ')
                        settings['mmer'][x[1].lower()] = x[2]
                        cl.sendMessage(to,'成功新增關鍵字')
                    elif cmd.startswith("刪關鍵 "):
                        x = text.split(' ')
                        del settings['mmer'][x[1].lower()]
                        cl.sendMessage(to,'成功刪除關鍵字\n'+str([x[1].lower()]))
                    elif cmd == '回覆列表':
                        if settings['mmer'] == {}:
                            cl.sendMessage(to, "沒有回復列表")
                        else:
                            mc = "[回覆列表]"
                            no = 1
                            for iii in settings['mmer']:
                                ttxt = settings['mmer']["{}".format(iii)]
                                mc += "\n"+str(no)+"."+iii+"\n"+str(ttxt)
                                no += 1
                            mc += "\n[總共 {} 個回覆]".format(str(no-1))
                            cl.sendMessage(to, str(mc))
                    elif cmd == '圖片回覆':
                        if settings['pic'] == {}:
                            cl.sendMessage(to, "沒有圖片回復")
                        else:
                            picture_reply_contents = [
                                {
                                    "type": "text",
                                    "text": "圖片回覆列表",
                                    "weight": "bold",
                                    "size": "lg",
                                    "color": "#000000",
                                    "margin": "md"
                                }
                            ]

                            # 添加圖片回覆項目
                            no = 1
                            for iii in settings['pic']:
                                picture_reply_contents.append({
                                    "type": "text",
                                    "text": "{}. {}".format(str(no), iii),
                                    "size": "md",
                                    "color": "#000000",
                                    "margin": "sm"
                                })
                                no += 1

                            # 總共的回覆數
                            picture_reply_contents.append({
                                "type": "text",
                                "text": "總共 {} 個回覆".format(str(no - 1)),
                                "size": "sm",
                                "color": "#888888",
                                "margin": "md",
                                "align": "end"
                            })

                            # 建立 Flex Message JSON 結構
                            flex_message = {
                                "type": "flex",
                                "altText": "圖片回覆列表",
                                "contents": {
                                    "type": "bubble",
                                    "body": {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": picture_reply_contents
                                    }
                                }
                            }
                            cl.sendLiff(to, flex_message)
                    elif cmd.startswith("delpic:"):
                        ieggm = cmd.replace("delpic:","")
                        if ieggm == "":
                            cl.sendMessage(to,"請輸入移除圖片關鍵字")
                        elif ieggm not in settings["pic"]:
                            cl.sendMessage(to,"找不到此關鍵字回復圖片")
                        else:
                            ooowwwoooo=settings["pic"][ieggm.lower()]
                            del settings["pic"][ieggm.lower()]
                            ddddd=ieggm+".jpg"
                            os.remove("picsave/"+ddddd)
                            cl.sendMessage(to,"已刪除以下關鍵字\n【"+str(ieggm)+"】\n刪除完畢")
                    elif cmd.startswith("addpic:"):
                        iggm = cmd.replace("addpic:","")
                        if iggm == "":
                            cl.sendMessage(to,"請輸入偵測圖片關鍵字")
                        elif iggm in settings["pic"]:
                            cl.sendMessage(to,"已有此關鍵字回覆的圖片")
                        else:
                            ooowwwooo = iggm+".jpg"
                            wait["xin"] = ooowwwooo
                            settings["pic"][iggm.lower()] = ooowwwooo
                            wait["akane"] = True
                            fkubao.append(sender)
                            cl.sendMessage(to,"請發送關鍵字\n【"+str(iggm)+"】\n要回覆的圖片")
                    elif cmd == "加企鵝":
                        wait["penguin"][sender] = True
                        cl.sendMessage(to, "請傳送penguin圖片")
                        return
                    elif cmd == "簽到重置":
                        group = cl.getChats([to]).chats[0]
                        try:
                            signin["ggrrp"][group.chatMid]=[]
                            cl.sendMention(to,"@!簽到重置成功",[sender])
                        except Exception as e:cl.sendMessage(to,e)
                    elif cmd == "簽到關閉":
                        group = cl.getChats([to]).chats[0]
                        try:
                            del signin["ggrrp"][group.chatMid]
                            cl.sendMention(to,"@!簽到關閉成功",[sender])
                        except Exception as e:cl.sendMessage(to,e)
                    elif cmd == '標記未簽到':
                        if to not in signin["ggrrp"]:cl.sendMessage(to,"未設置簽到")
                        else:
                            group = cl.getChats([to]).chats[0]
                            tagallignore=[]
                            for mem in group.extra.groupExtra.memberMids:
                                if mem in signin["ggrrp"][to]:pass
                                else:tagallignore.append(mem)
                            k = len(tagallignore)//20
                            for a in range(k+1):
                                txt = u''
                                s=0
                                b=[]
                                for i in tagallignore[a*20 : (a+1)*20]:
                                    b.append({"S":str(s), "E" :str(s+6), "M":i})
                                    s += 7
                                    txt += u'@LOVE \n'
                                if tagallignore == []:cl.sendMessage(to,"此群全部人都有簽到")
                                else:cl.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                    elif cmd == '簽到名單':
                        G = cl.getChats([to]).chats[0]
                        if G.chatMid not in signin["ggrrp"] or signin["ggrrp"][G.chatMid]==[]:
                            cl.sendMessage(to,"沒有簽到名單")
                        else:
                            try:
                                mc = "[ 以下為簽到名單 ]\n"
                                no = 0 
                                vvv=0
                                for mi_d in signin["ggrrp"][G.chatMid]:
                                    vvv+=1
                                    try:
                                        no += 1                                 
                                        mc += "{}. ".format(str(no))+ cl.getContact(mi_d).displayName + "\n"
                                    except:
                                        mc += "{}. ".format(str(no))+ "已經砍帳ㄌ\n"
                                    if vvv == 100:
                                        cl.sendMessage(to, mc)
                                        mc = "[ 以下為簽到名單 ]\n"
                                        vvv=0
                                    else:pass
                                mc += "\n[ 總共"+str(len(signin["ggrrp"][to]))+"個人簽到 ]"
                                cl.sendMessage(to, mc)
                            except:pass
                    elif cmd  == '未簽到名單':
                        if msg.toType == 2:
                            G = cl.getChats([to]).chats[0]
                            if G.chatMid not in signin["ggrrp"] or signin["ggrrp"][G.chatMid]==[]:cl.sendMessage(to,"沒有人簽到")
                            else:
                                ret_ = "[ 以下為未簽到名單 ]"
                                no = 1
                                for mem in G.extra.groupExtra.memberMids:
                                    if mem in signin["ggrrp"][G.chatMid]:pass
                                    else:
                                        abcm=cl.getContact(mem)
                                        ret_ += "\n{}. {}".format(str(no), str(abcm.displayName))
                                        no += 1
                                ret_ += "\n[ 未簽到共 {} 人]".format(str(no-1))
                                cl.sendMessage(to, str(ret_))
###################################################################################機器自身
                    elif cmd == "設定頭貼":
                        wait["changePictureProfile"][sender] = True
                        cl.sendMessage(to, "請傳送圖片")
                        return
                    elif cmd == "設定封面":
                        wait["changeCoverProfile"][sender] = True
                        cl.sendMessage(to, "請傳送圖片")
                        return
                    elif cmd.startswith('更改名稱'):
                            key = text[5:]
                            if len(text[3:]) <= 20:
                                cl.updateProfileAttribute(2, str(key))
                                cl.replyMessage(msg,"[提示]\n名稱改為\n"+str(key))
                            else:
                               cl.replyMessage(msg, '[提示]\n名稱無法超過20字喔!!')   
                    elif cmd.startswith('更改bio'):
                            key = text[6:]
                            if len(text[3:]) <= 500:
                              cl.updateProfileAttribute(16, str(key))
                              cl.replyMessage(msg,"[提示]\n個簽改為\n"+str(key))
                            else:
                              cl.replyMessage(msg,"[提示]\n個簽無法超過500字喔!!")
###################################################################################機器自身
                    elif text is not None and text.startswith("新增權限 "):
                        metdata = msg.contentMetadata
                        if 'MENTION' in metdata:
                            key = eval(metdata["MENTION"])
                            tags = key['MENTIONEES']
                            for tag in tags:
                                if tag['M'] not in settings['admin']:
                                    settings['admin'].append(tag['M'])
                                    cl.sendMessage(to, "成功新增權限")
                                else:
                                    cl.sendMessage(to, "權限已存在")
                            Save()
                    elif text is not None and text.startswith("刪除權限 "):
                        metdata = msg.contentMetadata
                        if 'MENTION' in metdata:
                            key = eval(metdata["MENTION"])
                            tags = key['MENTIONEES']
                            for tag in tags:
                                if tag['M'] in settings['admin']:
                                    settings['admin'].append(tag['M'])
                                    cl.sendMessage(to, "成功新增權限")
                                else:
                                    cl.sendMessage(to, "權限已存在")
                            Save()
                    elif text is not None and text.startswith("新增群管 "):
                        if to in settings['chatadmin']:...
                        else:
                            settings['chatadmin'][to] = []
                        metdata = msg.contentMetadata
                        if 'MENTION' in metdata:
                            key = eval(metdata["MENTION"])
                            tags = key['MENTIONEES']
                            for tag in tags:
                                if tag['M'] not in settings['chatadmin'][to]:
                                    settings['chatadmin'][to].append(tag['M'])
                                    cl.sendMessage(to, "成功新增權限")
                                else:
                                    cl.sendMessage(to, "權限已存在")
                            Save()
                    elif text is not None and text.startswith("刪除群管 "):
                        metdata = msg.contentMetadata
                        if 'MENTION' in metdata:
                            key = eval(metdata["MENTION"])
                            tags = key['MENTIONEES']
                            for tag in tags:
                                if tag['M'] in settings['chatadmin'][to]:
                                    settings['chatadmin'][to].remove(tag['M'])
                                    cl.sendMessage(to, "成功刪除權限")
                                else:
                                    cl.sendMessage(to, "權限不存在")
                            Save()
                    elif text is not None and text.startswith("tg:"):
                        ret = "Chat Member"
                        n = 0
                        chat = text[3:]
                        chats = cl.getChats([chat]).chats[0]
                        chats_member = chats.extra.groupExtra.memberMids
                        for x in chats_member:
                            n+=1
                            ret += f"\n{n}. {cl.getContact(x).displayName} | {x}"
                        cl.sendMessage(to, ret)
                    elif text is not None and text.startswith("mgqr:"):
                        n = 0
                        qr = text[5:]
                        cl.sendMessage(to,"請等待qr產生")
                        threading.Thread(target=traceRun(to,qr,)).start()
                    elif text is not None and text.startswith("tgc:"):
                        n = 0
                        chat = text[4:]
                        chats = cl.getChats([chat]).chats[0]
                        chats_member = chats.extra.groupExtra.memberMids
                        for x in chats_member:
                            cl.sendContact(to, x)
                    elif text is not None and text.startswith("tgi:"):
                        ret = "Chat Invitee"
                        n = 0
                        chat = text[4:]
                        chats = cl.getChats([chat]).chats[0]
                        chats_invitee = chats.extra.groupExtra.inviteeMids
                        for x in chats_invitee:
                            n+=1
                            ret += f"\n{n}. {cl.getContact(x).displayName} | {x}"
                        cl.sendMessage(to, ret)
                    elif text is not None and text.startswith("tgic:"):
                        chat = text[5:]
                        chats = cl.getChats([chat]).chats[0]
                        chats_invitee = chats.extra.groupExtra.inviteeMids
                        for x in chats_invitee:
                            cl.sendContact(to, x)
                    elif text is not None and text.startswith("邀請 "):
                        separate = text.split(" ")
                        number = text.replace(separate[0] + " ","")
                        groups = cl.getAllChatMids().memberChatMids
                        lists = list(groups)
                        try:
                            gid = lists[int(number)-1]
                            chat = cl.getChats([gid]).chats[0]
                            # chat.chatName
                            cl.addFriendByMid(sender)
                            cl.inviteIntoChat(gid, [sender])
                            cl.sendMessage(to, f"已邀請至: {chat.chatName} 群組",relatedMessageId=msg_id)
                        except Exception as e:cl.sendMessage(to, "邀請失敗:{}".format(str(e)),relatedMessageId=msg_id)
                    elif text is not None and text.startswith("退群 "):
                        separate = text.split(" ")
                        number = text.replace(separate[0] + " ","")
                        groups = cl.getAllChatMids().memberChatMids
                        lists = list(groups)
                        try:
                            gid = lists[int(number)-1]
                            chat = cl.getChats([gid]).chats[0]
                            # chat.chatName
                            cl.deleteSelfFromChat(gid)
                            cl.sendMessage(to, f"已退出: {chat.chatName} 群組",relatedMessageId=msg_id)
                        except Exception as e:cl.sendMessage(to, "退出失敗:{}".format(str(e)),relatedMessageId=msg_id)
                    
                    elif cmd == "alist":
                        # 假设企鵝的图片 URL
                            penguin_image_url = "https://i.imgur.com/dardtid.jpeg"

                            # 获取管理员列表的 Flex Message 内容
                            admin_list_contents = [
                                {
                                    "type": "text",
                                    "text": "[Admin List]",
                                    "weight": "bold",
                                    "size": "lg",
                                    "color": "#000000",
                                    "margin": "md"
                                }
                            ]

                            n = 0
                            for x in settings['admin']:
                                try:
                                    contact = cl.getContact(x)
                                    n += 1
                                    admin_list_contents.append({
                                        "type": "text",
                                        "text": "{}. {}".format(str(n), contact.displayName),
                                        "size": "md",
                                        "color": "#000000",
                                        "margin": "md"
                                    })
                                except Exception as e:
                                    print(e)

                            # 创建 Flex Message 的 JSON 结构
                            flex_message = {
                                "type": "flex",
                                "altText": "Admin List",
                                "contents": {
                                    "type": "bubble",
                                    "hero": {
                                        "type": "image",
                                        "url": penguin_image_url,
                                        "size": "full",
                                        "aspectRatio": "20:13",
                                        "aspectMode": "cover"
                                    },
                                    "body": {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": admin_list_contents
                                    }
                                }
                            }
                            cl.sendLiff(to, flex_message)
                    elif cmd == "lg":
                        chat_info = [f"{i+1}.{chat.chatName}|{chat.chatMid}\n\n" for i, chat_mid in enumerate(cl.getAllChatMids().memberChatMids) for chat in cl.getChats([chat_mid]).chats]
                        for i in range(0, len(chat_info), 30):
                            partial_chat_info = chat_info[i:i+30]
                            txt = "[Group List]\n" + "".join(partial_chat_info).rstrip()
                            cl.replyMessage(msg, txt)
                    elif cmd == "已讀開":
                        if to not in read["readed"]:
                            read["readed"][to] = []
                            cl.sendMessage(to,"偵測已讀開啟")
                        else:
                            cl.sendMessage(to,"偵測已經開啟囉")
                    elif cmd == "已讀關":
                        if to in read["readed"]:
                            del read["readed"][to]
                            cl.sendMessage(to,"偵測已讀關閉")
                        else:
                            cl.sendMessage(to,"偵測已經關閉囉")
                    elif cmd == "設置已讀":
                        if to not in read["readed2"]:
                            read["readed2"][to] = []
                            read["backread"][to] = ""
                            cl.sendMessage(to,"已讀點設置")
                        else:
                            cl.sendMessage(to,"已設置已讀點囉")
                    elif cmd == "刪除已讀":
                        if to in read["readed2"]:
                            del read["readed2"][to]
                            del read["backread"][to]
                            cl.sendMessage(to,"已讀點刪除")
                        else:
                            cl.sendMessage(to,"沒有設置已讀點")
                    elif cmd == 'ren':cl.sendLiff(to,botruntime_flex())
                    elif cmd == 'data':
                        #cl.downloadObjectMsg(msg_id,path="cv.jpg")
                        if msg.relatedMessageId:
                                try:
                                    for x in cl.getRecentMessagesV2(to,1000):
                                        if x.id == msg.relatedMessageId:
                                            cl.sendMessage(to,x,relatedMessageId=msg_id)
                                except:cl.sendMessage(to,"查詢失敗",relatedMessageId=msg_id)
                    elif cmd == 'qrs':
                        #cl.downloadObjectMsg(msg_id,path="cv.jpg")
                        if msg.relatedMessageId:
                                try:
                                    cl.downloadObjectMsg(msg.relatedMessageId,path="qrs.jpg")
                                    def scan_qr_code(image_path):
                                        with open(image_path, "rb") as image_file:
                                            files = {'image': image_file}
                                            response = requests.post("https://cloud.magiclen.org/api/qrcode/scan", files=files).json()
                                            if response.get("data"):
                                                return response["data"][0]  # 返回成功的數據
                                            else:
                                                return None
                                    a = scan_qr_code(f"qrs.jpg")
                                    cl.sendMessage(to,str(a),relatedMessageId=msg_id)
                                except:cl.sendMessage(to,"查詢失敗",relatedMessageId=msg_id)
                if sender in sender and is_spamming(sender):pass
                else:
                    ids = re.findall(ALLIDS_REGEX,cmd)
                    if len(ids) > 0:
                        idss=0
                        for _id in ids:
                            if _id.startswith('u'):  # 如果ID以 'u' 开头
                                cl.sendContact(to,str(_id))
                                idss+=1
                                time.sleep(0.5)
                    if game_state["active"] == True:
                        if cmd.isdigit():  # 检查输入是否为数字
                            response = handle_guess(cmd)
                            cl.replyMessage(msg, response)
                    #公開指令
                    if cmd == "清空標註":
                        tag_file = f"tag/{sender}.json"
                        try:
                            os.remove(tag_file)
                            cl.sendMessage(to,"成功")
                        except Exception as e:print(f"Error: {e}")
                    if cmd in cities:
                        data = requests.get("https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=rdec-key-123-45678-011121314").json()
                        index = cities.index(text)
                        Wx = data["records"]["location"][index]["weatherElement"][0]["time"][0]["parameter"]["parameterName"]
                        PoP = data["records"]["location"][index]["weatherElement"][1]["time"][0]["parameter"]["parameterName"]
                        MinT = data["records"]["location"][index]["weatherElement"][2]["time"][0]["parameter"]["parameterName"]
                        CI = data["records"]["location"][index]["weatherElement"][3]["time"][0]["parameter"]["parameterName"]
                        MaxT = data["records"]["location"][index]["weatherElement"][4]["time"][0]["parameter"]["parameterName"]
                        flex_message_json = {
                            "type": "flex",
                            "altText": f"{text} 的天氣狀況",
                            "contents": {
                                "type": "bubble",
                                "header": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": f"{text} 天氣狀況",
                                            "weight": "bold",
                                            "size": "lg",
                                            "align": "center"
                                        }
                                    ]
                                },
                                "body": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                                {"type": "text", "text": "天氣", "weight": "bold", "size": "md", "flex": 1},
                                                {"type": "text", "text": Wx, "size": "md", "flex": 2}
                                            ]
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                                {"type": "text", "text": "最高溫", "weight": "bold", "size": "md", "flex": 1},
                                                {"type": "text", "text": f"{MaxT} 度", "size": "md", "flex": 2}
                                            ]
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                                {"type": "text", "text": "最低溫", "weight": "bold", "size": "md", "flex": 1},
                                                {"type": "text", "text": f"{MinT} 度", "size": "md", "flex": 2}
                                            ]
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                                {"type": "text", "text": "降雨機率", "weight": "bold", "size": "md", "flex": 1},
                                                {"type": "text", "text": f"{PoP} %", "size": "md", "flex": 2}
                                            ]
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                                {"type": "text", "text": "體感", "weight": "bold", "size": "md", "flex": 1},
                                                {"type": "text", "text": CI, "size": "md", "flex": 2}
                                            ]
                                        }
                                    ]
                                }
                            }
                        }

                        cl.sendLiff(to,flex_message_json)
                    if cmd == '誰標我':
                        tag_file = f"tag/{sender}.json"
                        if os.path.isfile(tag_file):
                            with codecs.open(tag_file, "r", "utf-8") as f:
                                who_mark_me = json.load(f)
                            if to in who_mark_me:
                                tag_num = len(who_mark_me[to])
                                try:
                                    contact = cl.getContact(str(who_mark_me[to][str(tag_num)]["sender"]))
                                    message = (
                                        f"上一位標註者\n"
                                        f"{contact.displayName}\n"
                                        f"時間：{who_mark_me[to][str(tag_num)]['tagtime']}\n"
                                        f"剩餘查詢次數：{tag_num - 1}"
                                    )
                                    cl.sendMessage(msg.to, message, relatedMessageId=who_mark_me[to][str(tag_num)]["msgid"])
                                    del who_mark_me[to][str(tag_num)]
                                    with codecs.open(tag_file, "w", "utf-8") as f:
                                        json.dump(who_mark_me, f, sort_keys=True, indent=4, ensure_ascii=False)
                                except Exception as e:print(f"Error: {e}")
                    elif cmd == "開始":
                        response = start_game()
                        cl.replyMessage(msg,response)
                    elif text is not None and text.startswith("企鵝小幫手 "):
                        separate = text.split(" ")
                        number = text.replace(separate[0] + " ","")
                        from g4f.client import Client
                        client = Client()
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{"role": "user", "content": number}],
                            # Add any other necessary parameters
                        )
                        cl.sendMessage(to, response.choices[0].message.content)
                    elif cmd == "抽塔羅":
                        txt = random.choice(tarot_readings)
                        flex_content = {"type": "flex","altText": "塔羅牌","contents": {"type": "bubble","body": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "你抽到的塔羅牌","weight": "bold","size": "lg","color": "#000000","margin": "md"},{"type": "text","text": txt,"weight": "bold","size": "md","color": "#1E90FF","margin": "md","wrap": True},{"type": "separator","margin": "xl"}]}}}
                        cl.sendLiff(to,flex_content)
                    elif cmd == "抽運勢":
                        ptoday=draw_lucky_penguin()
                        txt=random.choice(daily_horoscope["fortunes"])
                        flex_content = {"type": "flex","altText": "今日幸運企鵝","contents": {"type": "bubble","body": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "今日幸運企鵝是：","weight": "bold","size": "lg","color": "#000000","margin": "md"},{"type": "text","text": ptoday,"weight": "bold","size": "xl","color": "#1E90FF","margin": "md"},{"type": "separator","margin": "xl"},{"type": "text","text": txt,"size": "md","color": "#000000","wrap": True,"margin": "lg"}]}}}
                        cl.sendLiff(to,flex_content)
                    elif cmd == "抽自訂":
                        ptoday=draw_lucky_penguin2()
                        txt=random.choice(daily_horoscope["fortunes"])
                        flex_content = {"type": "flex","altText": "今日幸運企鵝","contents": {"type": "bubble","body": {"type": "box","layout": "vertical","contents": [{"type": "text","text": "今日幸運企鵝是：","weight": "bold","size": "lg","color": "#000000","margin": "md"},{"type": "text","text": ptoday,"weight": "bold","size": "xl","color": "#1E90FF","margin": "md"},{"type": "separator","margin": "xl"},{"type": "text","text": txt,"size": "md","color": "#000000","wrap": True,"margin": "lg"}]}}}
                        cl.sendLiff(to,flex_content)
                    elif cmd == "簽到":
                        group = cl.getChats([to]).chats[0].chatMid
                        if group in signin["ggrrp"]:
                            if sender in signin["ggrrp"][group]:
                                cl.sendMention(to,"@!您已簽到完成 不需重複簽到",[sender])
                            else:
                                signin["ggrrp"][group].append(sender)
                                cl.sendMention(to,"@!簽到成功！",[sender])
                                Save()
                        else:pass
                    elif cmd == "簽":
                        group = cl.getChats([to]).chats[0].chatMid
                        if group in signin["ggrrp"]:
                            if sender in signin["ggrrp"][group]:
                                pass
                                cl.sendMention(to,"@!您已簽到完成 不需重複簽到",[sender])
                            else:
                                signin["ggrrp"][group].append(sender)
                                cl.sendMention(to,"@!簽到成功！",[sender])
                                Save()
                        else:pass
                    elif cmd == "當前狀態":
                        contents = []
                        for key, value in status.items():
                            contents.append({
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": str(key),
                                        "color": "#111111",
                                        "size": "md",
                                        "flex": 2
                                    },
                                    {
                                        "type": "text",
                                        "text": str(value),
                                        "color": "#111111",
                                        "size": "md",
                                        "align": "end",
                                        "flex": 3
                                    }
                                ]
                            })

                            flex_message555 = {
                                "type": "flex",
                                "altText": "狀態信息",
                                "contents": {
                                    "type": "bubble",
                                    "body": {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "狀態信息",
                                                "weight": "bold",
                                                "size": "xl",
                                                "align": "center"
                                            },
                                            {
                                                "type": "box",
                                                "layout": "vertical",
                                                "margin": "lg",
                                                "spacing": "sm",
                                                "contents": contents
                                            }]}}}
                        cl.sendLiff(to, flex_message555)
                    elif cmd == "成長":
                        play_adventure(msg,to)
                    elif cmd == "抽賤倉":
                        for _, _, files in os.walk(r'fuck'):
                            print("檔案：", files)
                        sample=random.choice(files)
                        cl.sendImage(to,"fuck/"+sample)
                        pic = sum(len(files) for _, _, files in os.walk(r'fuck'))
                    elif cmd in choices:
                        cl.sendLiff(to,play_rps(sender,cmd))
                    elif cmd =="分數":
                        if sender in user_scores:
                            score = user_scores[sender]
                            flex_content = {
                                "type": "flex",
                                "altText": "你的當前分數",
                                "contents": {
                                    "type": "bubble",
                                    "body": {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "你的當前分數",
                                                "weight": "bold",
                                                "size": "xl",
                                                "align": "center"
                                            },
                                            {
                                                "type": "box",
                                                "layout": "vertical",
                                                "margin": "lg",
                                                "spacing": "sm",
                                                "contents": [
                                                    {
                                                        "type": "box",
                                                        "layout": "baseline",
                                                        "spacing": "sm",
                                                        "contents": [
                                                            {
                                                                "type": "text",
                                                                "text": "贏",
                                                                "color": "#111111",
                                                                "size": "md",
                                                                "flex": 2
                                                            },
                                                            {
                                                                "type": "text",
                                                                "text": str(score['win']),
                                                                "color": "#111111",
                                                                "size": "md",
                                                                "align": "end",
                                                                "flex": 1
                                                            }
                                                        ]
                                                    },
                                                    {
                                                        "type": "box",
                                                        "layout": "baseline",
                                                        "spacing": "sm",
                                                        "contents": [
                                                            {
                                                                "type": "text",
                                                                "text": "輸",
                                                                "color": "#111111",
                                                                "size": "md",
                                                                "flex": 2
                                                            },
                                                            {
                                                                "type": "text",
                                                                "text": str(score['lose']),
                                                                "color": "#111111",
                                                                "size": "md",
                                                                "align": "end",
                                                                "flex": 1
                                                            }
                                                        ]
                                                    },
                                                    {
                                                        "type": "box",
                                                        "layout": "baseline",
                                                        "spacing": "sm",
                                                        "contents": [
                                                            {
                                                                "type": "text",
                                                                "text": "平手",
                                                                "color": "#111111",
                                                                "size": "md",
                                                                "flex": 2
                                                            },
                                                            {
                                                                "type": "text",
                                                                "text": str(score['draw']),
                                                                "color": "#111111",
                                                                "size": "md",
                                                                "align": "end",
                                                                "flex": 1
                                                            }]}]}]}}}
                            cl.sendLiff(to,flex_content)
                        else:
                            cl.replyMessage(msg,"你還沒有遊戲紀錄。")
                    elif "鮑魚" in cmd and "吃" in cmd and to == "cef1824a855c6a78bc442491ec2e695ed":
                        cl.replyMessage(msg,"吃你的嗎?")
                    elif "棉" in cmd and sender not in cl.profile.mid:cl.replyMessage(msg,"你也是企鵝嗎")
                    elif "倉鼠" in cmd:cl.replyMessage(msg,"你也想被吱療嗎")
                    elif "老哥" in cmd:cl.replyMessage(msg,"不犯賤了 不犯賤了")
                    if cmd == 'mymid':
                            cl.replyMessage(msg,cl.getContact(sender).mid)
                    if cmd == 'gid':
                            cl.replyMessage(msg,cl.getChats([to]).chats[0].chatMid)
                    elif cmd == "大樂透":
                        lottery = TaiwanLotteryCrawler()
                        result = lottery.lotto649()
                        data539 = {
                            "type": "flex",
                            "altText": "Lottery Results",
                            "contents": {
                                "type": "bubble",
                                "body": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "Lottery Results",
                                            "weight": "bold",
                                            "size": "xl",
                                            "align": "center"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "期別",
                                                    "color": "#aaaaaa",
                                                    "size": "sm"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": str(result[0]["期別"]),
                                                    "size": "sm",
                                                    "align": "end"
                                                }
                                            ]
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "開獎日期",
                                                    "color": "#aaaaaa",
                                                    "size": "sm"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": result[0]["開獎日期"][:10],  # 確保只顯示日期部分
                                                    "size": "sm",
                                                    "align": "end"
                                                }
                                            ]
                                        },
                                        {
                                            "type": "separator",
                                            "margin": "md"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "margin": "md",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "大樂透開獎號碼",
                                                    "weight": "bold",
                                                    "size": "md",
                                                    "align": "center"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": ', '.join(map(str, result[0]["獎號"])),  # 將號碼列表轉換為字符串
                                                    "size": "lg",
                                                    "align": "center",
                                                    "margin": "md"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "特別號",
                                                    "weight": "bold",
                                                    "size": "md",
                                                    "align": "center"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": str(result[0]["特別號"]),  # 將號碼列表轉換為字符串
                                                    "size": "lg",
                                                    "align": "center",
                                                    "margin": "md"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                        cl.sendLiff(to, data539)
                    elif cmd == "539":
                        lottery = TaiwanLotteryCrawler()
                        result = lottery.daily_cash()
                        data539 = {
                            "type": "flex",
                            "altText": "Lottery Results",
                            "contents": {
                                "type": "bubble",
                                "body": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "Lottery Results",
                                            "weight": "bold",
                                            "size": "xl",
                                            "align": "center"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "期別",
                                                    "color": "#aaaaaa",
                                                    "size": "sm"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": str(result[0]["期別"]),
                                                    "size": "sm",
                                                    "align": "end"
                                                }
                                            ]
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "開獎日期",
                                                    "color": "#aaaaaa",
                                                    "size": "sm"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": result[0]["開獎日期"][:10],  # 確保只顯示日期部分
                                                    "size": "sm",
                                                    "align": "end"
                                                }
                                            ]
                                        },
                                        {
                                            "type": "separator",
                                            "margin": "md"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "margin": "md",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "539 開獎號碼",
                                                    "weight": "bold",
                                                    "size": "md",
                                                    "align": "center"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": ', '.join(map(str, result[0]["獎號"])),  # 將號碼列表轉換為字符串
                                                    "size": "lg",
                                                    "align": "center",
                                                    "margin": "md"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            }
                        }
                        cl.sendLiff(to, data539)
                    elif cmd in settings['mmer']: 
                        cl.sendMessage(to,settings['mmer'][cmd])
                    elif cmd in settings['pic'] and sender not in cl.profile.mid:
                        jjjjj=settings['pic'][cmd]
                        ppppp="picsave/"+jjjjj
                        cl.sendImage(to,ppppp)
                    elif cmd == "抽企鵝":
                        for _, _, files in os.walk(r'penguin'):
                            print("檔案：", files)
                        sample=random.choice(files)
                        cl.sendImage(to,"penguin/"+sample)
                        pic = sum(len(files) for _, _, files in os.walk(r'penguin'))
                        ret_ =f"🌠企鵝圖片：{pic} 張"
                        cl.sendMessage(to, str(ret_),op.message.id)
                    elif cmd == 'rlb':
                        slots = generate_slots()
                        flex_contents = [
                            {
                                "type": "text",
                                "text": "拉霸機拉霸一次",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#000000"
                            }
                        ]
                        # 添加每一行的结果
                        for i, row in enumerate(slots):
                            flex_contents.append({
                                "type": "text",
                                "text": f"第{i+1}行 ==> {row[0]}  {row[1]}  {row[2]} <==",
                                "size": "md",
                                "color": "#000000",
                                "margin": "md"
                            })

                        # 检查是否中奖
                        winner = check_winner(slots)
                        if winner:
                            flex_contents.append({
                                "type": "text",
                                "text": f"\n恭喜！第 {winner} 行中獎！",
                                "size": "md",
                                "color": "#FF0000",
                                "weight": "bold",
                                "margin": "lg"
                            })
                        else:
                            flex_contents.append({
                                "type": "text",
                                "text": "\n很遺憾，沒有中獎。",
                                "size": "md",
                                "color": "#000000",
                                "margin": "lg"
                            })

                        # 构建完整的 Flex Message JSON
                        flex_message = {
                            "type": "flex",
                            "altText": "拉霸機結果",
                            "contents": {
                                "type": "bubble",
                                "body": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": flex_contents
                                }
                            }
                        }
                        cl.sendLiff(to, flex_message)
                    elif cmd.startswith('loginsqr'):
                                x = text.split(' ')
                                a = CHRLINE(device="DESKTOPWIN", noLogin=True)
                                for b in a.requestSQR():
                                    cl.sendMessage(to, str(b))
                                    try:
                                        cl.sendImage(to,"login.jpg")
                                        os.remove("login.jpg")
                                    except:pass
                                if a.authToken:
                                    #_bot.sendMessage(msg[2], '登入成功')
                                    cl.sendMessage(to,a.authToken)
                                    bc = CHRLINE(a.authToken,device="DESKTOPWIN")
                                 
                                    #wait["bc"][sender] = True
                                    chats = bc.getChats([x[1]]).chats[0]
                                    cl.sendMessage(to,bc.getContact(bc.mid).displayName+"\n\n廣播機登入成功\n目標群組\n\n"+chats.chatName+"\n\n共"+str(len(chats.extra.groupExtra.memberMids)))
                                    chats_member = chats.extra.groupExtra.memberMids
                                    count=0
                                    for mid in chats_member:
                                        bc.sendMessage(mid,x[2])
                                        #bc.createPost(mid,x[2])
                                        count+=1
                                        time.sleep(1.5)
                                    cl.sendMessage(to,'成功'+str(count)+"人")
                    elif cmd is not None and cmd.startswith("抽人 "):
                            ret = '[抽到的人]'
                            randomList = []
                            randomList2 = []
                            for x in cl.getChats([to]).chats[0].extra.groupExtra.memberMids:
                                randomList.append(x)
                            for x in range(int(text[3:])):
                                ret+='\n@!'
                            b = random.sample(randomList,int(text[3:]))
                            cl.sendMention(to,ret,b)
                    elif cmd == 'help':
                        data={
                            "type": "flex",
                            "altText": "歡迎機指令表",
                            "contents": {
                                "type": "bubble",
                                "hero": {
                                    "type": "image",
                                    "url": "https://plus.unsplash.com/premium_photo-1661813041159-d9608ffac3ae?q=80&w=1767&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                                    "size": "full",
                                    "aspectRatio": "20:13",
                                    "aspectMode": "cover"
                                },
                                "body": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "企鵝歡迎機指令表🐧",
                                            "weight": "bold",
                                            "size": "xl",
                                            "color": "#000000",
                                            "margin": "md"
                                        },
                                        {
                                            "type": "text",
                                            "text": "==管理員指令表==",
                                            "weight": "bold",
                                            "size": "md",
                                            "color": "#000000",
                                            "margin": "md"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                                { "type": "text", "text": "新增權限 @/刪除權限 @" },
                                                { "type": "text", "text": "設定進群:文字 設定進群訊息" },
                                                { "type": "text", "text": "(標註記得@!)" },
                                                { "type": "text", "text": "設定退群:文字 設定退群訊息(同上)" },
                                                { "type": "text", "text": "設定進群圖片" },
                                                { "type": "text", "text": "設定退群圖片" },
                                                { "type": "text", "text": "設定頭貼 更改機器頭貼" },
                                                { "type": "text", "text": "設定封面 更改機器封面" },
                                                { "type": "text", "text": "已讀開/關 即時抓已讀開關" },
                                                { "type": "text", "text": "設置已讀 設置已讀點" },
                                                { "type": "text", "text": "刪除已讀 刪除已讀點" },
                                                { "type": "text", "text": "查詢已讀 已讀點誰已讀" },
                                                { "type": "text", "text": "更改名稱 更改機器名稱" },
                                                { "type": "text", "text": "更改bio 更改機器自介" },
                                                { "type": "text", "text": "加企鵝 加企鵝圖片" },
                                                { "type": "text", "text": "關鍵 text text/刪關鍵 text" },
                                                { "type": "text", "text": "addpic:text/delpic:text/圖片回覆" },
                                                { "type": "text", "text": "公告 查公告" },
                                                { "type": "text", "text": "igp:url/igv:url ig下載功能" },
                                                { "type": "text", "text": "簽到關閉/簽到重置 群組簽到功能" },
                                                { "type": "text", "text": "bye 退群" }
                                            ]
                                        },
                                        {
                                            "type": "text",
                                            "text": "==無權限指令表==",
                                            "weight": "bold",
                                            "size": "md",
                                            "color": "#000000",
                                            "margin": "md"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                                { "type": "text", "text": "誰標我 來看看是誰標你" },
                                                { "type": "text", "text": "rlb 拉霸機" },
                                                { "type": "text", "text": "抽賤倉" },
                                                { "type": "text", "text": "抽自訂" },
                                                { "type": "text", "text": "開始 開始猜數字遊戲" },
                                                { "type": "text", "text": "抽企鵝" },
                                                { "type": "text", "text": "石頭/剪刀/布 猜拳" },
                                                { "type": "text", "text": "分數 猜拳分數" },
                                                { "type": "text", "text": "抽塔羅 抽塔羅牌" },
                                                { "type": "text", "text": "成長/當前狀態 桌寵功能" },
                                                { "type": "text", "text": "清空標註" },
                                                { "type": "text", "text": "539 看539開獎結果" },
                                                { "type": "text", "text": "大樂透 看大樂透開獎結果" },
                                                { "type": "text", "text": "抽人 數字    抽獎功能" },
                                                { "type": "text", "text": "mymid/gid 查個人內碼/群組內碼" },
                                                { "type": "text", "text": "企鵝小幫手 文字  ai功能" },
                                                { "type": "text", "text": "簽/簽到 簽到" }
                                            ]
                                        },
                                        {
                                            "type": "text",
                                            "text": "有任何BUG請盡速回報",
                                            "size": "sm",
                                            "color": "#ff5555",
                                            "margin": "md"
                                        },
                                        {
                                            "type": "button",
                                            "style": "link",
                                            "height": "sm",
                                            "action": {
                                                "type": "uri",
                                                "label": "作者聯繫方式",
                                                "uri": "https://line.me/ti/p/LNqlk10SCo"
                                            }}]}}}
                        cl.sendLiff(to,data)
        if msg.contentType == 0:#文字
                try:
                    msg_dict[msg_id] = {"text":text,"from":sender,"createdTime":msg.createdTime}
                except:pass
        if msg.contentType == 1:#圖片
                try:
                    image = cl.downloadObjectMsg(msg_id, path="file/image/{}-jpg.jpg".format(msg.createdTime))
                    image_dict[msg_id] = {"from":sender,"image":image,"createdTime":msg.createdTime}
                except:pass
                
        if msg.contentType == 2:#影片
                try:
                    Video = cl.downloadObjectMsg(msg_id, path="file/video/{}-Video.mp4".format(msg.createdTime))
                    video_dict[msg_id] = {"from":sender,"Video":Video,"createdTime":msg.createdTime}
                except:pass
        if msg.contentType == 3:#語音
                try:
                    audio = cl.downloadObjectMsg(msg_id, path="file/audio/{}-Audio.mp3".format(msg.createdTime))
                    audio_dict[msg_id] = {"from":sender,"Audio":audio,"createdTime":msg.createdTime}
                except:pass
        if msg.contentType == 7:#貼圖
                try:
                    sticker_dict[msg_id] = {"from":sender,"id":msg.contentMetadata['STKID'],"createdTime":msg.createdTime}
                except:pass
        if msg.contentType == 13:#友資
                try:
                    contact_dict[msg_id] = {"from":sender,"mid":msg.contentMetadata,"createdTime":msg.createdTime}
                except:pass
        if msg.contentType == 14:#檔案
                try:
                    file = cl.downloadObjectMsg(msg_id, path="file/file/{}-File".format(msg.createdTime))
                    file_dict[msg_id] = {"from":sender,"file":file,"createdTime":msg.createdTime}
                except:pass
        else:...
        
        if msg.contentType == 1:
            if sender in wait['changePictureProfile']:
                cl.downloadObjectMsg(msg_id,path='cp.jpg')
                cl.updateProfileImage("cp.jpg")
                cl.replyMessage(msg, "更改頭貼成功")
                time.sleep(1);os.remove("cp.jpg")         
                del wait["changePictureProfile"][sender]
            if wait["akane"] == True:
                if sender in fkubao:
                    ooowwwoooo = wait["xin"]
                    jjjj = cl.downloadObjectMsg(msg_id, path="picsave/"+ooowwwoooo)
                    wait["xin"] = ""
                    wait["akane"] = False
                    fkubao.clear()
                    cl.sendMessage(msg.to,"圖片回覆新增完成")
            elif sender in wait['bc']:
                import uuid
                filename = f"{uuid.uuid4()}.jpg"
                cl.downloadObjectMsg(msg_id,path="bc"+"/"+filename+".jpg")
                cl.replyMessage(msg, "储存成功")      
                del wait["bc"][sender]
            elif sender in wait['penguin']:
                import uuid
                filename = f"{uuid.uuid4()}.jpg"
                cl.downloadObjectMsg(msg_id,path="penguin"+"/"+filename+".jpg")
                cl.replyMessage(msg, "增加企鵝成功")      
                del wait["penguin"][sender]
            elif sender in wait["changeCoverProfile"]:
                cl.downloadObjectMsg(msg_id,path="cv.jpg")
                cl.updateProfileCover("cv.jpg")
                cl.replyMessage(msg, "更改封面成功")
                del wait["changeCoverProfile"][sender]
            elif sender in wait["changeChatJoinPicture"]:
                cl.downloadObjectMsg(msg_id,path=f"Join/{to}.jpg")
                settings['welcomepic'][to] = f"Join/{to}.jpg"
                Save()
                cl.replyMessage(msg, "更改成功")
                del wait["changeChatJoinPicture"][sender]
            elif sender in wait["changeChatLeavePicture"]:
                cl.downloadObjectMsg(msg_id,path=f"Leave/{to}.jpg")
                settings['leavepic'][to] = f"Leave/{to}.jpg"
                Save()
                cl.replyMessage(msg, "更改成功")
                del wait["changeChatLeavePicture"][sender]
            
    elif op.type == 60:
        if op.param1 not in settings['welcome']:
            return
        else:
            if "@!" in settings['welcome'][op.param1]:
                cl.sendMention(op.param1,settings['welcome'][op.param1],op.param2)
                if settings['welcomepic'][op.param1] == "":return
                else:cl.sendImage(op.param1,settings['welcomepic'][op.param1])
            else:
                cl.sendMessage(op.param1,settings['welcome'][op.param1])
                if settings['welcomepic'][op.param1] == "":return
                else:cl.sendImage(op.param1,settings['welcomepic'][op.param1])
    elif op.type == 61:
        if op.param1 not in settings['leave']:
            return
        else:
            if "@!" in settings['leave'][op.param1]:
                cl.sendMention(op.param1,settings['leave'][op.param1],op.param2)
                if settings['leavepic'][op.param1] == "":return
                else:cl.sendImage(op.param1,settings['leavepic'][op.param1])
            else:
                cl.sendMessage(op.param1,settings['leave'][op.param1])
                if settings['leavepic'][op.param1] == "":return
                else:cl.sendImage(op.param1,settings['leavepic'][op.param1])
    elif op.type == 65:
            chat=cl.getChats([op.param1]).chats[0]
            if op.param2 in msg_dict:
                if 'text' in msg_dict[op.param2]:
                    rereadtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(round(msg_dict[op.param2]["createdTime"]/1000))))
                    newtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    aa = '{"S":"0","E":"3","M":'+json.dumps(msg_dict[op.param2]["from"])+'}'
                    txr = '[收回訊息]\n%s\n[發送時間]\n%s\n[收回時間]\n%s'%(msg_dict[op.param2]["text"],rereadtime,newtime)
                    pesan = '@c \n'
                    text_ =  pesan + "群組名稱："+ str(chat.chatName) + "\n" + txr
                    cl.sendMessage(backdoor, text_ , contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
                    del msg_dict[op.param2]
            if op.param2 in image_dict:
                if 'image' in image_dict[op.param2]:
                    rereadtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(round(image_dict[op.param2]["createdTime"]/1000))))
                    newtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    aa = '{"S":"0","E":"3","M":'+json.dumps(image_dict[op.param2]["from"])+'}'
                    txr = '[收回了一張圖片]\n在下面\n[發送時間]\n%s\n[收回時間]\n%s'%(rereadtime,newtime)
                    pesan = '@c \n'
                    text_ =  pesan + "群組名稱："+ str(chat.chatName) + "\n" + txr
                    cl.sendMessage(backdoor, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
                    cl.sendImage(backdoor, image_dict[op.param2]["image"])
                    del image_dict[op.param2]
            if op.param2 in video_dict:
                if 'Video' in video_dict[op.param2]:
                    rereadtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(round(video_dict[op.param2]["createdTime"]/1000))))
                    newtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    aa = '{"S":"0","E":"3","M":'+json.dumps(video_dict[op.param2]["from"])+'}'
                    txr = '[收回了一部影片]\n在下面\n[發送時間]\n%s\n[收回時間]\n%s'%(rereadtime,newtime)
                    pesan = '@c \n'
                    text_ =  pesan + "群組名稱："+ str(chat.chatName) + "\n" + txr
                    cl.sendMessage(backdoor, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
                    cl.sendVideo(backdoor, video_dict[op.param2]["Video"])
                    del video_dict[op.param2]
            if op.param2 in audio_dict:
                if 'Audio' in audio_dict[op.param2]:
                    rereadtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(round(audio_dict[op.param2]["createdTime"]/1000))))
                    newtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    aa = '{"S":"0","E":"3","M":'+json.dumps(audio_dict[op.param2]["from"])+'}'
                    txr = '[收回了一段語音]\n在下面\n[發送時間]\n%s\n[收回時間]\n%s'%(rereadtime,newtime)
                    pesan = '@c \n'
                    text_ =  pesan + "群組名稱："+ str(chat.chatName) + "\n" + txr
                    cl.sendMessage(backdoor, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
                    cl.sendAudio(backdoor, audio_dict[op.param2]["Audio"])
                    del audio_dict[op.param2]
            if op.param2 in sticker_dict:
                if 'id' in sticker_dict[op.param2]:
                    rereadtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(round(sticker_dict[op.param2]["createdTime"]/1000))))
                    newtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    aa = '{"S":"0","E":"3","M":'+json.dumps(sticker_dict[op.param2]["from"])+'}'
                    txr = '[收回了一張貼圖]\n在下面\n[發送時間]\n%s\n[收回時間]\n%s'%(rereadtime,newtime)
                    pesan = '@c \n'
                    text_ =  pesan + "群組名稱："+ str(chat.chatName) + "\n" + txr
                    cl.sendMessage(backdoor , text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
                    ok = 'https://stickershop.line-scdn.net/stickershop/v1/sticker/' + sticker_dict[op.param2]["id"] + '/ANDROID/sticker.png'
                    cl.sendImage(backdoor, ok)
                    del sticker_dict[op.param2]
            if op.param2 in contact_dict:
                if 'mid' in contact_dict[op.param2]:
                    rereadtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(round(contact_dict[op.param2]["createdTime"]/1000))))
                    newtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    aa = '{"S":"0","E":"3","M":'+json.dumps(contact_dict[op.param2]["from"])+'}'
                    txr = '[收回了一個友資]\n在下面\n[發送時間]\n%s\n[收回時間]\n%s'%(rereadtime,newtime)
                    pesan = '@c \n'
                    text_ =  pesan + "群組名稱："+ str(chat.chatName) + "\n" + txr
                    cl.sendMessage(backdoor, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
                    cl.sendContact(backdoor, contact_dict[op.param2]["mid"]["mid"])
                    del contact_dict[op.param2]
            if op.param2 in file_dict:
                if 'file' in file_dict[op.param2]:
                    rereadtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(round(file_dict[op.param2]["createdTime"]/1000))))
                    newtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    aa = '{"S":"0","E":"3","M":'+json.dumps(file_dict[op.param2]["from"])+'}'
                    txr = '[收回了一個檔案]\n在下面\n[發送時間]\n%s\n[收回時間]\n%s'%(rereadtime,newtime)
                    pesan = '@c \n'
                    text_ =  pesan + "群組名稱："+ str(chat.chatName) + "\n" + txr
                    cl.sendMessage(backdoor, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
                    cl.sendFile(backdoor, file_dict[op.param2]["file"])
                    del file_dict[op.param2]
    elif op.type == 124:
        chat=cl.getChats([op.param1]).chats[0]
        if cl.profile.mid in op.param3:
            print(f"[{op.type}] [邀請入群]")
            try:
                threading.Thread(target=cl.acceptChatInvitation,args=(op.param1,)).start()
                ret="★[提示]有人邀我至群組"
                ret+=f"\n★群組名稱:{chat.chatName}"
                ret+=f"\n★群組ID:{chat.chatMid}"
                ret+=f"\n★邀請者:{cl.getContact(op.param2).displayName}"
                ret+=f"\n★邀請者ID:{cl.getContact(op.param2).mid}"
                ret+=f"\n★群組人數:{len(chat.extra.groupExtra.memberMids)}"
                cl.sendMessage(backdoor,ret)
            except Exception as e:print(e)
            
while True:
    try:threading.Thread(target=cl.trace(bot)).start()
    except KeyboardInterrupt:break