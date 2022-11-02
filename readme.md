# saveAssetImage

## 概要

- Windows10のロック画面の壁紙をjpgファイルで保管してくれるサービスです。
- バージョン: 3.10.1
- 使用ライブラリ
  - pywin32
  - watchdog
  - Pillow

## インストール

1. 任意のフォルダにクローンする。
2. venv環境を作成し、activateする。
3. `pip install -r requirements.txt`
4. `python [クローンしたフォルダ]\Scripts\pywin32_postinstall.py -install`を実行する。
5. `\Lib\site-packages\win32\pythonservice.exe`を`\Scripts\pythonservice.exe`にコピーする。
6. 管理者権限で、`python saveAssetImage.py install`を実行する。

## 実行

1. サービスを開き、「壁紙保管サービス」に引数を指定して開始する。
   - 引数1: コピー元のフォルダのパス(Windowsのロック画面のファイルが作成されるフォルダ)
   - 引数2: コピー先のフォルダのパス(任意のフォルダ)

## アンインストール

1. サービスを開き、「壁紙保管サービス」を停止する。
2. 管理者権限で、`python saveAssetImage.py remove`を実行する。
3. クローンしたフォルダを削除する。
