# 車庫映像モニター 作成手順書（初心者向け）

この手順書では、Raspberry Pi のテレビ画面に車庫映像を全画面表示するまでを説明します。

## 1. 目的

作りたいもの:

- 車庫カメラの映像を Raspberry Pi で受信
- テレビに Chromium で全画面表示
- 起動後に自動表示

## 2. 前提

以下を前提にしています。

- Raspberry Pi が起動済み
- デスクトップ画面が使える
- 車庫カメラ映像 URL がある
- 例: `http://192.168.0.55:8080/?action=stream`

## 3. フォルダ作成

```bash
mkdir -p /home/pi/garage_monitor
cd /home/pi/garage_monitor
```

このフォルダに以下のファイルを置きます。

- `garage_viewer.html`
- `start_garage_monitor.sh`
- `garage-monitor.desktop`

## 4. HTML の役割

`garage_viewer.html` は、車庫映像を表示する画面本体です。

主な役割:

- 映像を表示する
- タイトルを表示する
- 日時を表示する

映像元の URL はこの行です。

```html
<img src="http://192.168.0.55:8080/?action=stream" alt="Garage Camera Stream">
```

ここを自分の環境に合わせて変更してください。

## 5. 起動スクリプトの役割

`start_garage_monitor.sh` は Chromium を全画面で起動するためのスクリプトです。

実行権限を付けます。

```bash
chmod +x /home/pi/garage_monitor/start_garage_monitor.sh
```

手動で動かすには:

```bash
/home/pi/garage_monitor/start_garage_monitor.sh
```

## 6. 自動起動設定

ログイン時に自動で表示するため、`.desktop` ファイルを使います。

まずフォルダを作ります。

```bash
mkdir -p ~/.config/autostart
```

次にコピーします。

```bash
cp /home/pi/garage_monitor/garage-monitor.desktop ~/.config/autostart/
```

これで、再起動後に自動で車庫モニターが起動します。

## 7. よくある失敗

### 7-1. 映像が出ない
原因:
- カメラ URL が違う
- 車庫カメラ側が起動していない

対策:
- Chromium で URL を直接開いて確認する

### 7-2. Chromium が開かない
原因:
- デスクトップにログインしていない
- 起動タイミングが早すぎる

対策:
- `sleep 10` を `sleep 15` にする

### 7-3. 画面が真っ黒
原因:
- URL に誤り
- カメラのストリーム形式が違う

対策:
- `?action=stream` の有無を確認
- ブラウザで直接試す

## 8. GitHub 掲載について

このフォルダはそのまま GitHub に掲載できます。

ただし以下は含めないでください。

- token
- password
- credentials.json
- 個人情報

## 9. まとめ

この仕組みでやっていることはシンプルです。

1. カメラ映像 URL を用意する
2. HTML に書く
3. Chromium で全画面表示する
4. 自動起動にする

最初から完璧にする必要はありません。
まず映像が出ることを目標にしてください。
