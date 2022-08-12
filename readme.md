# saveAssetImage

## 概要

- Windowsのロック画面の壁紙をjpgファイルで保管してくれるサービスです。
- バージョン: 3.10
- 使用ライブラリ
  - pywin32
  - watchdog

## インストール

1. 任意のフォルダにクローンする。
2. - システム環境変数のPathに以下のパスを追加する。
```
C:\Users\{ユーザー名}\AppData\Local\Programs\Python\Python{バージョン}\
C:\Users\{ユーザー名}\AppData\Local\Programs\Python\Python{バージョン}\Scripts\
C:\Users\{ユーザー名}\AppData\Local\Programs\Python\Python{バージョン}\Lib\site-packages\pywin32_system32
C:\Users\{ユーザー名}\AppData\Local\Programs\Python\Python{バージョン}\Lib\site-packages\win32
```
3. クローンしたフォルダでコマンドプロンプトを管理者権限で実行し、以下のコマンドを実行する。
```
python saveAssetImage.py install
```

## 実行

1. サービスを開き、「壁紙保管サービス」に引数を指定して開始する。
  - 引数1: コピー元のフォルダのパス(Windowsのロック画面のファイルが作成されるフォルダ)
  - 引数2: コピー先のフォルダのパス(任意のフォルダ)

## アンインストール

1. サービスを開き、「壁紙保管サービス」を停止する。
2. クローンしたフォルダでコマンドプロンプトを管理者権限で実行し、以下のコマンドを実行する。
```
python saveAssetImage.py remove
```
3. クローンしたフォルダを削除する。