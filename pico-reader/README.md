Pico W MQTT受信確認サンプル

Raspberry Pi Pico W を Wi-Fi に接続し、MQTTブローカーからメッセージを受信して、本体LEDで受信状態を確認するためのサンプルプログラムです。

Windows PC や Raspberry Pi などから MQTT メッセージを送信し、Pico W 側で正しく受信できるかを確認できます。

1. このプログラムの目的

このプログラムは、Pico W を MQTT の受信側として動作させる確認用プログラムです。

主な確認内容は次の通りです。

Pico W が Wi-Fi に接続できるか
MQTTブローカーに接続できるか
指定した topic を購読できるか
Windows PC や Raspberry Pi から送信した MQTT メッセージを受信できるか
受信結果を Pico W 本体LEDで確認できるか
2. 全体構成
Windows PC / Raspberry Pi
        │
        │ MQTT送信
        ▼
MQTTブローカー
192.168.0.140:1883
        │
        │ topic: genkan/event
        ▼
Raspberry Pi Pico W
        │
        │ 受信内容に応じて制御
        ▼
Pico W 本体LED
3. 動作の流れ
Pico W 起動
   ↓
Wi-Fi に接続
   ↓
MQTTブローカー 192.168.0.140 に接続
   ↓
genkan/event を購読
   ↓
MQTT受信待機
   ↓
受信メッセージに応じて LED を操作
4. 使用環境
ハードウェア
Raspberry Pi Pico W
Wi-Fi環境
MQTTブローカーが動作している機器
例: Raspberry Pi
IPアドレス例: 192.168.0.140
ソフトウェア
MicroPython
umqtt.simple
MQTTブローカー
例: Mosquitto
MQTT送信用クライアント
Windows PC の mosquitto_pub
Raspberry Pi の mosquitto_pub
Node-RED など
5. プログラム設定内容
Wi-Fi設定
WIFI_SSID = "aterm-cebc72-g"
WIFI_PASSWORD = "********"

Pico W が接続する Wi-Fi の SSID とパスワードを設定します。

注意: README.md などで公開する場合、Wi-Fiパスワードは必ず伏せてください。

MQTT設定
BROKER = "192.168.0.140"
PORT = 1883
TOPIC = b"genkan/event"
CLIENT_ID = b"pico18"
項目	内容
BROKER	MQTTブローカーのIPアドレス
PORT	MQTT通信ポート。通常は 1883
TOPIC	受信するMQTTトピック
CLIENT_ID	MQTT接続時の機器識別名
6. CLIENT_ID の注意点

MQTTでは、同じブローカーに接続する機器の CLIENT_ID は必ず一意にする必要があります。

CLIENT_ID = b"pico18"

別のPico Wや別のMQTTクライアントで同じ CLIENT_ID を使用すると、接続が切れたり、不安定になったりします。

複数台のPico Wを使う場合は、次のように機器ごとに変更します。

CLIENT_ID = b"pico18"
CLIENT_ID = b"pico19"
CLIENT_ID = b"pico20"
7. 受信メッセージとLED動作

このプログラムでは、受信したメッセージに応じて Pico W 本体LEDを操作します。

受信メッセージ	LED動作
ON	LED点灯
OFF	LED消灯
その他	LED反転

例:

ON   → LED点灯
OFF  → LED消灯
TEST → LED反転
8. プログラム本体
import network
import time
from machine import Pin
from umqtt.simple import MQTTClient




# =========================
# Wi-Fi設定
# =========================
WIFI_SSID = "aterm-cebc72-g"
WIFI_PASSWORD = "********"




# =========================
# MQTT設定
# =========================
BROKER = "192.168.0.140"
PORT = 1883
TOPIC = b"genkan/event"


# MQTTのCLIENT_IDは機器ごとに必ず一意にする
CLIENT_ID = b"pico18"




# =========================
# 動作確認用LED
# =========================
led = Pin("LED", Pin.OUT)




# =========================
# Wi-Fi接続
# =========================
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)


    if not wlan.isconnected():
        print("Wi-Fi接続開始")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)


        timeout = 20


        while not wlan.isconnected() and timeout > 0:
            print("Wi-Fi待機中...")
            time.sleep(1)
            timeout -= 1


    if wlan.isconnected():
        print("Wi-Fi接続OK")
        print("IP:", wlan.ifconfig()[0])
        return wlan


    raise RuntimeError("Wi-Fi接続失敗")




# =========================
# MQTT受信時の処理
# =========================
def on_message(topic, msg):
    print("受信:", topic, msg)


    if msg == b"ON":
        led.value(1)
        print("LED ON")


    elif msg == b"OFF":
        led.value(0)
        print("LED OFF")


    else:
        led.toggle()
        print("LED toggle")




# =========================
9. 実行方法
1. Pico W に MicroPython を書き込む

Pico W に MicroPython ファームウェアを書き込みます。

2. Thonny で Pico W に接続する

Thonny を起動し、インタプリタを MicroPython Raspberry Pi Pico に設定します。

3. プログラムを保存する

Pico W 側に次の名前で保存します。

main.py

main.py として保存すると、Pico W 起動時に自動実行されます。

テスト中は、別名で保存して手動実行しても問題ありません。

例:

mqtt_receiver_test.py
10. Windows PC から MQTT送信テスト

Windows PC に Mosquitto クライアントが入っている場合、PowerShell から送信できます。

LEDを点灯する
mosquitto_pub -h 192.168.0.140 -t genkan/event -m ON
LEDを消灯する
mosquitto_pub -h 192.168.0.140 -t genkan/event -m OFF
LEDを反転する
mosquitto_pub -h 192.168.0.140 -t genkan/event -m TEST
11. Raspberry Pi から MQTT送信テスト

Raspberry Pi から送信する場合も、同じように実行できます。

mosquitto_pub -h 192.168.0.140 -t genkan/event -m ON
mosquitto_pub -h 192.168.0.140 -t genkan/event -m OFF
mosquitto_pub -h 192.168.0.140 -t genkan/event -m TEST
12. MQTTブローカー側で受信確認する方法

MQTTブローカー側、または別の端末で次のコマンドを実行すると、送信されたメッセージを確認できます。

mosquitto_sub -h 192.168.0.140 -t 'genkan/event' -v

表示例:

genkan/event ON
genkan/event OFF
genkan/event TEST
13. 正常動作時の表示例

Pico W 側の実行画面には、次のように表示されます。

Wi-Fi接続開始
Wi-Fi待機中...
Wi-Fi接続OK
IP: 192.168.0.18
MQTT接続開始
BROKER: 192.168.0.140
PORT: 1883
TOPIC: b'genkan/event'
CLIENT_ID: b'pico18'
client.connect() 実行前
client.connect() 実行後
MQTT接続OK
subscribe OK: b'genkan/event'
MQTT受信待機開始

MQTTを受信すると、次のように表示されます。

受信: b'genkan/event' b'ON'
LED ON
14. トラブル対応
client.connect() 実行前で止まる場合

以下を確認します。

確認項目	内容
ブローカーIP	192.168.0.140 が正しいか
MQTTブローカー	Mosquitto が起動しているか
ポート	1883 が使用できるか
Wi-Fi	Pico W とブローカーが同じネットワークにいるか
CLIENT_ID	他の機器と重複していないか
MQTTを受信しない場合

以下を確認します。

送信先 topic が genkan/event になっているか
Pico W 側の TOPIC と一致しているか
MQTTブローカーのIPアドレスが正しいか
Windows PC や Raspberry Pi からブローカーへ接続できるか
CLIENT_ID が重複していないか
LEDが点灯しない場合

以下を確認します。

Pico W 本体LEDを使っているか
led = Pin("LED", Pin.OUT) になっているか
受信メッセージが ON または OFF になっているか
on_message() が実行されているか
15. 応用例

このプログラムは、MQTT受信確認用の基本サンプルとして使用できます。

応用すると、次のような制御に発展できます。

インターホンイベント受信
玄関通知システム
LED表示器
リレー制御
ブザー制御
Node-RED との連携
複数Pico Wによるイベント受信
16. 今回の位置づけ

このプログラムは、実運用前の MQTT通信確認用です。

特に、次の確認に向いています。

Windows PC から MQTT送信
        ↓
MQTTブローカーで中継
        ↓
Pico W が受信
        ↓
LEDで受信確認

今後、インターホン・監視カメラ・散水制御などのシステムと連携する前の、基本確認用テンプレートとして利用できます。

17. 注意事項
Wi-Fiパスワードは公開しないでください。
CLIENT_ID は機器ごとに必ず変更してください。
同じ topic を複数の受信機で購読することは可能です。
ただし、CLIENT_ID が同じだと接続が競合します。
実運用では、受信後の処理をLEDではなくリレーや表示処理に変更できます。
18. ライセンス

個人利用・学習用途として自由に利用できます。

19. メモ

このサンプルでは、受信確認用として Pico W 本体LEDを使用しています。

本格運用時は、LED制御部分を目的に応じて変更します。

例:

if msg == b"ON":
    # リレーON、ブザーON、表示更新などに変更可能
    pass

README.md形式で編集しました。
