# Node-RED Flow for MQTT Doorbell Receiver

本ディレクトリは、Pico W から送信された MQTT イベントを  
Node-RED で受信・確認・処理するためのフローを提供します。

---

## ■ 概要

Pico W から送信される `doorbell` イベントを受信し、  
Node-RED 上で可視化および制御処理を行います。

```text
Pico W
↓
MQTT
↓
Node-RED
↓
表示 / 制御
