# raspberrypi-genkan-tv-system
# Raspberry Pi インターホン連動テレビシステム

本リポジトリは、Raspberry PiとPico Wを利用した  
インターホン連動テレビ表示システムのサンプルです。

## 構成

- Node-RED フロー
- Pico W スイッチ検知コード
- MQTT連携

## 使用方法

1. Node-REDでJSONをインポート
2. MQTT設定を変更
3. cec-clientを有効化
4. 動作確認

## フロー概要

インターホン → MQTT → Node-RED → TV制御

## 注意

環境に応じてIPアドレス等を変更してください。
