from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont

from python.service.recognition_service import RecognitionService
from python.util.image_util import ImageUtil
from python.util.text_recognition_thread import RecognitionThread
from python.util.ui_util import UiUtil


class RecognitionController:
    def __init__(self, main_window):
        self.main_window = main_window  # 保存对主窗口的引用
        self.recognition_menu = main_window.menubar.addMenu("识别")
        self.ui_tool = UiUtil()
        self.image_util = ImageUtil()
        self.image = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_text)
        self.count = 0
        self.recognition_service = RecognitionService(self.main_window)
        self.font = QFont()
        self.setup_recognition_menu_actions()

    def set_image(self, image):
        self.image = image

    def setup_recognition_menu_actions(self):
        # 这里添加所有识别菜单项
        actions = [
            ("文本识别", self.recognize_text),
            ("表格识别", self.recognize_table)
        ]
        for action_text, callback in actions:
            self.ui_tool.add_action(self.main_window,
                                    self.recognition_menu,
                                    action_text,
                                    callback)

    def recognize_text_init(self):
        self.font.setFamily('Microsoft YaHei')
        self.font.setPointSize(13)
        self.main_window.result_text.setFont(self.font)

    def update_text(self):
        self.timer.start(300)
        self.count += 1
        if self.count % 2 == 0:
            self.main_window.result_text.setText('识别中. . .')
        else:
            self.main_window.result_text.setText('识别中. . . . . .')

        if self.count >= 4:
            self.timer.stop()
            self.count = 0

    def recognize_text(self):
        self.main_window.result_text.setText('')
        self.recognize_text_init()
        self.update_text()
        # 创建新的线程来执行文本识别
        self.recognition_thread = RecognitionThread(self.image, self.recognition_service)
        self.recognition_thread.textRecognized.connect(self.on_text_recognized)
        self.recognition_thread.start()

    def on_text_recognized(self, text):
        self.main_window.result_text.setText(text)

    def recognize_table(self):
        self.recognition_service.recognize_table(self.image)
