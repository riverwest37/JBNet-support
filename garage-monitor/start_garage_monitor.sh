#!/bin/bash

# 車庫モニター全画面起動スクリプト
# 必要に応じて DISPLAY や XAUTHORITY を環境に合わせて変更してください

sleep 10

chromium \
  --kiosk \
  --noerrdialogs \
  --disable-infobars \
  --disable-session-crashed-bubble \
  --user-data-dir=/tmp/chromium-garage-monitor \
  file:///home/pi/garage_monitor/garage_viewer.html
