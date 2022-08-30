import logging
import os
import shutil
import socket
import sys
import time

script_path = os.path.dirname(__file__)
sys.path.append(os.path.join(script_path, "Lib\site-packages"))
sys.path.append(os.path.join(script_path, "Lib\site-packages\win32\lib"))

import servicemanager
import win32event
import win32service
import win32serviceutil
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from PIL import Image

win32serviceutil.ServiceFramework._exe_name_ = os.path.join(os.path.join(script_path , "Scripts", 'pythonservice.exe'))

logging.basicConfig(
    filename = '.\\saveAssetImage.log',
    level = logging.DEBUG, 
    format="%(asctime)s: %(levelname)s %(message)s"
)

# サービス
class MySvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "saveAssetImage"
    _svc_display_name_ = "壁紙保管サービス"
    _svc_description_='ロック画面の画像を保管する'

    # 初期化
    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.stop_event = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False
        self.args = args

    # サービス停止
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        logging.info('停止リクエストを受け付けました')
        self.stop_requested = True

    # サービス開始
    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_,'')
        )

        self.main_loop()

    def main_loop(self):
        logging.info('サービスを開始しました')

        if not len(self.args) == 3 :
            logging.error('引数エラー サービスを停止します')
            return
        
        logging.info('コピー元：%s' % self.args[1])
        logging.info('コピー先：%s' % self.args[2])
        event_handler = ChangeHandler(self.args[2])
        observer = Observer()
        observer.schedule(event_handler, self.args[1], recursive=True)
        observer.start()

        while True:
            if self.stop_requested:
                logging.info('サービス停止中...')
                observer.stop()
                break

            time.sleep(0.1)
        
        observer.join()
        logging.info("サービスを停止しました")
        return

# フォルダ監視
class ChangeHandler(FileSystemEventHandler):

    def __init__(self, target_dir):
        self.target_dir = target_dir

    # ファイル作成時、保管先にコピーする
    def on_created(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        logging.info('%sが作成されました' % filename)
        while not os.access(filepath,os.W_OK):
            time.sleep(0.5)
        try:
            time.sleep(0.5)
            im = Image.open(filepath)
            width, height = im.size
            if width > height :
                shutil.copy(filepath, os.path.join(self.target_dir, filename + ".jpg"))
                logging.info('%sをコピーしました' % filename)
        except Exception as e:
            logging.error(e)

    # ファイル変更時 ログ出力のみ
    def on_modified(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        logging.info('%sが変更されました' % filename)

    # ファイル削除時 ログ出力のみ
    def on_deleted(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        logging.info('%sが削除されました' % filename)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MySvc)
