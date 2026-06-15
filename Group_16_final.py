from gpiozero import Button, LED
from signal import pause
from datetime import datetime
import json
import socket
import paho.mqtt.client as mqtt

# =========================
# LINE 新增
# =========================
import os
import sys
import requests
from dotenv import load_dotenv

# 載入 .env
load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")

LINE_PUSH_ENDPOINT = "https://api.line.me/v2/bot/message/push"

# 如果 LINE 沒設定好，不讓整個系統中斷，只是提醒
LINE_ENABLE = True

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_USER_ID:
    print("LINE 尚未設定完成：請在 .env 設定 LINE_CHANNEL_ACCESS_TOKEN 和 LINE_USER_ID")
    print("系統仍會繼續執行，但不會發送 LINE 訊息")
    LINE_ENABLE = False


# ==================================================
# MQTT 設定
# ==================================================

MQTT_BROKER = "rpi5-16.local"
MQTT_PORT = 1883
MQTT_TOPIC = "final"

mqtt_client = mqtt.Client(client_id="rpi5_emergency_system")

# ==================================================
# GPIO 設定
# ==================================================

# 緊急事件按鈕
btn_lab = Button(17, pull_up=True, bounce_time=0.2)
btn_dorm = Button(27, pull_up=True, bounce_time=0.2)

# LED
led_lab = LED(21)
led_dorm = LED(20)

DEVICE_ID = socket.gethostname()

# ==================================================
# 狀態管理
# ==================================================

location_status = {
    "lab": "normal",
    "dorm": "normal"
}

location_names = {
    "lab": "70404 教室",
    "dorm": "Dorm 宿舍"
}

# ==================================================
# 時間
# ==================================================

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ==================================================
# LINE 發送訊息
# ==================================================

def send_line_message(text):

    if not LINE_ENABLE:
        return

    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
        }

        body = {
            "to": LINE_USER_ID,
            "messages": [
                {
                    "type": "text",
                    "text": text
                }
            ]
        }

        response = requests.post(
            LINE_PUSH_ENDPOINT,
            headers=headers,
            json=body,
            timeout=10
        )

        if response.status_code == 200:
            print("LINE message sent successfully")
        else:
            print("LINE message failed")
            print("status:", response.status_code)
            print("response:", response.text)

    except Exception as e:
        print("LINE send error:", e)


# ==================================================
# 建立事件 JSON
# ==================================================

def create_event(location_id, status):

    timestamp = get_timestamp()

    location_name = location_names[location_id]

    event_id = f"{location_id}_{timestamp.replace(' ', '_').replace(':', '')}"

    # 狀態訊息
    if status == "triggered":
        message = f"{location_name} 發生緊急事件"
        resolved_time = ""

    elif status == "resolved":
        message = f"{location_name} 緊急事件已處理完成"
        resolved_time = timestamp

    else:
        message = f"{location_name} 狀態正常"
        resolved_time = ""

    event = {
        "event_id": event_id,
        "timestamp": timestamp,
        "device_id": DEVICE_ID,
        "location_id": location_id,
        "location_name": location_name,
        "event_type": "Emergency",
        "status": status,
        "message": message,
        "resolved_time": resolved_time
    }

    return event


# ==================================================
# LED 控制
# ==================================================

def update_led(location_id):

    if location_id == "lab":

        if location_status["lab"] == "triggered":
            led_lab.on()
        else:
            led_lab.off()

    elif location_id == "dorm":

        if location_status["dorm"] == "triggered":
            led_dorm.on()
        else:
            led_dorm.off()


# ==================================================
# 發送 MQTT
# ==================================================

def publish_to_mqtt(event):

    try:

        payload = json.dumps(event, ensure_ascii=False)

        result = mqtt_client.publish(
            MQTT_TOPIC,
            payload,
            qos=1,
            retain=True
        )

        if result.rc == mqtt.MQTT_ERR_SUCCESS:

            print("\nMQTT Publish Success")
            print("Topic:", MQTT_TOPIC)

            print(json.dumps(event, ensure_ascii=False, indent=2))

        else:
            print("MQTT publish failed")

    except Exception as e:
        print("MQTT publish error:", e)


# ==================================================
# 緊急事件處理
# ==================================================

def handle_emergency(location_id):

    location_name = location_names[location_id]

    # 避免重複觸發
    if location_status[location_id] == "triggered":

        print(f"{location_name} 已經是警報中")
        return

    # 更新狀態
    location_status[location_id] = "triggered"

    # LED 更新
    update_led(location_id)

    # 建立事件
    event = create_event(location_id, "triggered")

    # 發送 MQTT 給 Dashboard
    publish_to_mqtt(event)

    # 發送 LINE 給自己
    line_text = (
        "🚨 緊急事件通知\n"
        f"地點：{event['location_name']}\n"
        f"時間：{event['timestamp']}\n"
        f"設備：{event['device_id']}\n"
        f"狀態：{event['status']}\n"
        f"訊息：{event['message']}"
    )

    send_line_message(line_text)


# ==================================================
# 接收 MQTT（Dashboard Resolve）
# ==================================================

def on_message(client, userdata, msg):

    try:

        payload = json.loads(msg.payload.decode())

        location_id = payload.get("location_id")

        status = payload.get("status")

        # 只處理 resolved
        if status == "resolved":

            # 如果這個 resolved 已經有 resolved_time，
            # 代表它可能是 Python 自己剛剛 publish 出去的，不要再重複處理
            if payload.get("resolved_time"):
                return

            print(f"\n{location_id} resolved from dashboard")

            # 更新狀態
            location_status[location_id] = "normal"

            # LED 熄滅
            update_led(location_id)

            # 建立 resolved event
            event = create_event(location_id, "resolved")
            print(json.dumps(event, ensure_ascii=False, indent=2))

            # 發送給 Dashboard，讓 dashboard 顯示處理完成時間
            publish_to_mqtt(event)

    except Exception as e:
        print("MQTT receive error:", e)


# ==================================================
# MQTT Connect
# ==================================================

def on_connect(client, userdata, flags, rc):

    if rc == 0:

        print("MQTT connected successfully")

        # 訂閱 topic
        client.subscribe(MQTT_TOPIC)

        print("Subscribed to:", MQTT_TOPIC)

    else:
        print("MQTT connection failed")


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# ==================================================
# 啟動 MQTT
# ==================================================

try:

    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

    mqtt_client.loop_start()

except Exception as e:

    print("MQTT connection error:", e)


# ==================================================
# 初始狀態
# ==================================================

def publish_initial_status():

    for location_id in location_status:

        location_status[location_id] = "normal"

        update_led(location_id)

        event = create_event(location_id, "normal")

        publish_to_mqtt(event)

# ==================================================
# GPIO Button 綁定
# ==================================================

btn_lab.when_pressed = lambda: handle_emergency("lab")

btn_dorm.when_pressed = lambda: handle_emergency("dorm")


# ==================================================
# 系統啟動
# ==================================================

print("\n===================================")
print("AIoT Emergency System Started")
print("===================================")

print("GPIO17 → lab 教室按鈕")
print("GPIO27 → Dorm 宿舍按鈕")

print("GPIO21 → 教室 LED")
print("GPIO20 → 宿舍 LED")

print("MQTT Topic:", MQTT_TOPIC)

print("Waiting for emergency buttons...\n")

# 初始化 dashboard 狀態
publish_initial_status()

pause()