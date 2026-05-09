📟 lcd_date.py - CO₂センサー & LCD表示 + LINE通知システム
概要
このスクリプトは、Raspberry Pi に接続された以下のデバイスを用いて、現在時刻とCO₂濃度をLCDに表示し、濃度に応じてLEDを点滅させたり、閾値を超えた場合にはLINEに警告通知を送信するシステムです。

🧰 使用機器・部品
Raspberry Pi（GPIOピン付き）

I2C接続 LCD（アドレス: 0x3f）

MH-Z19 CO₂センサー（UART or USB変換で接続）

LED（2個：黄色、赤色）

抵抗（適宜）

LINE Bot アカウント（アクセストークンとユーザーIDが必要）

📦 必要なPythonパッケージ
以下のパッケージが必要です。インストールされていない場合は事前にインストールしてください。

bash
コピーする
編集する
sudo pip3 install mh-z19 requests
また、smbus は次のコマンドでインストールできます（未インストール時）:

bash
コピーする
編集する
sudo apt-get install python3-smbus
🔧 ファイル構成
bash
コピーする
編集する
lcd_date.py              # 本体スクリプト
line_config.py           # LINEアクセストークン等を記載
📄 line_config.py の内容（別ファイル）
python
コピーする
編集する
# line_config.py
channel_access_token = "YOUR_CHANNEL_ACCESS_TOKEN"
to_user_id = "YOUR_USER_ID"
⚙️ 動作概要
LCD に現在日時と CO₂ 濃度をリアルタイムで表示

CO₂ 濃度が 1000〜1500 ppm → 黄色LEDが点滅

CO₂ 濃度が 1500 ppm 超え → 赤色LEDが点滅 & LINEに通知（30分おき）

Ctrl+C で停止すると LCDをクリアし GPIOをクリーンアップ

🖥️ 実行方法
bash
コピーする
編集する
python3 lcd_date.py
🔍 注意事項
mh_z19 ライブラリが正常に CO₂ センサーと通信できるよう、適切に接続してください。

line_config.py のアクセストークンやユーザーIDが正しいことを確認してください。

I2C LCD のアドレスは 0x3f ですが、環境により異なる可能性があるため、i2cdetect コマンドで確認してください。

bash
コピーする
編集する
sudo apt install i2c-tools
sudo i2cdetect -y 1
📌 参考
LINE Messaging API ドキュメント

MH-Z19 CO₂ センサー Pythonライブラリ
