# Garage Monitor Viewer for Raspberry Pi

このリポジトリは、車庫カメラ映像を Raspberry Pi の Chromium で全画面表示するための最小構成です。
GitHub にそのまま掲載できるように、HTML・起動スクリプト・自動起動設定・作成手順をまとめています。

## 1. 概要

この構成でできること:

- 車庫カメラの映像を 1 画面で表示
- Raspberry Pi 起動後に自動で Chromium を開く
- GitHub 上で配布・再利用しやすい構成

想定する車庫カメラの映像 URL 例:

- `http://192.168.0.55:8080/?action=stream`

必要に応じて `garage_viewer.html` 内の URL を変更してください。

## 2. ファイル説明

- `garage_viewer.html`
  - 車庫映像を表示する HTML
- `start_garage_monitor.sh`
  - Chromium を kiosk モードで起動するスクリプト
- `garage-monitor.desktop`
  - 自動起動用デスクトップ設定ファイル
- `INSTALL_JA.md`
  - 初心者向け作成手順書
- `.gitignore`
  - GitHub 公開時に不要ファイルを除外

## 3. すぐ試す方法

Raspberry Pi 上で次を実行します。

```bash
mkdir -p /home/pi/garage_monitor
```

このリポジトリの中身を `/home/pi/garage_monitor/` に置いてください。

実行権限を付けます。

```bash
chmod +x /home/pi/garage_monitor/start_garage_monitor.sh
```

手動起動:

```bash
/home/pi/garage_monitor/start_garage_monitor.sh
```

## 4. 自動起動

`garage-monitor.desktop` を次にコピーします。

```bash
mkdir -p ~/.config/autostart
cp /home/pi/garage_monitor/garage-monitor.desktop ~/.config/autostart/
```

これでログイン後に自動起動します。

## 5. カメラ URL の変更

`garage_viewer.html` の次の行を探してください。

```html
<img src="http://192.168.0.55:8080/?action=stream" alt="Garage Camera Stream">
```

使用中の車庫カメラ URL に変更します。

## 6. GitHub 掲載時の使い方

このフォルダをそのまま GitHub にアップロードできます。

推奨リポジトリ名例:

- `garage-monitor-viewer`
- `raspi-garage-monitor`

README と手順書を含んでいるので、そのまま配布用として使えます。

## 7. 注意

- 個人情報、トークン、パスワードは含めないでください。
- グローバル IP や認証情報は GitHub に掲載しないでください。
- ローカル IP (`192.168.x.x`) は例としては問題ありませんが、実運用では適宜読み替えてください。
