import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# secrets.py から読み込む
import secrets

# =============================
# 設定読み込み
# =============================
WIFI_SSID = secrets.WIFI_SSID
WIFI_PASSWORD = secrets.WIFI_PASSWORD

BROKER = secrets.BROKER
PORT = secrets.PORT
TOPIC = secrets.TOPIC
CLIENT_ID = secrets.CLIENT_ID

# =============================
# GPIO設定
# =============================
BUTTON_PIN = 15
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

# =============================
# Wi-Fi接続
# =============================
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        print("Wi-Fi接続中...")
        while not wlan.isconnected():
            time.sleep(1)

    print("Wi-Fi接続完了:", wlan.ifconfig())
    return wlan

# =============================
# MQTT接続
# =============================
def connect_mqtt():
    client = MQTTClient(CLIENT_ID, BROKER, port=PORT)
    client.connect()
    print("MQTT接続完了:", BROKER)
    return client

# =============================
# メイン処理
# =============================
def main():
    connect_wifi()
    client = connect_mqtt()

    # 起動時の現在状態を取得
    last_state = button.value()

    print("ボタン監視開始")

    while True:
        current_state = button.value()

        # 押された瞬間（1 → 0）
        if last_state == 1 and current_state == 0:
            try:
                payload = '{"type":"doorbell"}'
                client.publish(TOPIC, payload)
                print("doorbell送信")

            except Exception as e:
                print("MQTT送信エラー:", e)

                # 再接続して再送
                try:
                    client = connect_mqtt()
                    client.publish(TOPIC, payload)
                    print("再送成功")
                except Exception as e2:
                    print("再送失敗:", e2)

            # 押しっぱなし防止（離されるまで待つ）
            while button.value() == 0:
                time.sleep(0.05)

        # 前回状態更新
        last_state = current_state

        # CPU負荷軽減
        time.sleep(0.05)

# =============================
# 起動
# =============================
main()
