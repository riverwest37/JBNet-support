# main.py
import network
import time
import socket
from machine import Pin
from umqtt.simple import MQTTClient

# =========================
# Wi-Fi 設定
# =========================
WIFI_SSID = "あなたのSSID"
WIFI_PASSWORD = "あなたのパスワード"

# =========================
# MQTT 設定
# =========================
BROKER = "192.168.0.xxx"
PORT = 1883
TOPIC = b"genkan/event"

# 正規稼働中の picow-doorbell と重複させない
CLIENT_ID = b"picow-doorbell-test18"

# Pico W 本体LED
led = Pin("LED", Pin.OUT)


# =========================
# Wi-Fi 接続
# =========================
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Wi-Fi接続中...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        for i in range(20):
            if wlan.isconnected():
                break
            print(".", end="")
            time.sleep(1)

    if wlan.isconnected():
        print()
        print("Wi-Fi接続OK")
        print("IP:", wlan.ifconfig()[0])
        return wlan
    else:
        print()
        print("Wi-Fi接続NG")
        return None


# =========================
# TCP 接続テスト
# =========================
def test_tcp():
    print("TCP接続テスト開始...")

    try:
        s = socket.socket()
        s.settimeout(5)
        s.connect((BROKER, PORT))
        s.close()

        print("TCP接続OK:", BROKER, PORT)
        return True

    except Exception as e:
        print("TCP接続NG:", e)
        return False


# =========================
# MQTT 受信時の処理
# =========================
def mqtt_callback(topic, msg):
    print()
    print("MQTT受信")
    print("TOPIC:", topic)
    print("MSG:", msg)

    # メッセージ確認用LED動作
    if msg == b"ON":
        led.on()
        print("LED ON")

    elif msg == b"OFF":
        led.off()
        print("LED OFF")

    else:
        # その他のメッセージは短く点滅
        led.on()
        time.sleep(0.2)
        led.off()


# =========================
# MQTT 接続
# =========================
def connect_mqtt():
    print("MQTT接続開始")
    print("BROKER:", BROKER)
    print("PORT:", PORT)
    print("TOPIC:", TOPIC)
    print("CLIENT_ID:", CLIENT_ID)

    client = MQTTClient(
        client_id=CLIENT_ID,
        server=BROKER,
        port=PORT,
        keepalive=30
    )

    client.set_callback(mqtt_callback)

    print("client.connect() 実行")
    client.connect(clean_session=True)
    print("client.connect() 成功")

    client.subscribe(TOPIC)
    print("subscribe 成功:", TOPIC)

    return client


# =========================
# メイン処理
# =========================
wlan = connect_wifi()

if wlan is None:
    print("Wi-Fiに接続できないため停止します")
    while True:
        led.toggle()
        time.sleep(1)

if not test_tcp():
    print("MQTT Broker の1883番に接続できません")
    while True:
        led.toggle()
        time.sleep(0.5)

client = connect_mqtt()

print()
print("MQTT受信待機中...")

while True:
    try:
        # MQTTメッセージ確認
        client.check_msg()
        time.sleep(0.1)

    except Exception as e:
        print()
        print("MQTTエラー:", e)
        print("再接続します")

        try:
            client.disconnect()
        except:
            pass

        time.sleep(3)

        wlan = connect_wifi()

        if wlan is not None and test_tcp():
            client = connect_mqtt()
