from PyQt5.QtCore import QThread, pyqtSignal
from paddleocr import PPStructure
from logger import logger

class TableRecognitionThread(QThread):
    recognition_complete = pyqtSignal(object)
    recognition_failed = pyqtSignal(str)  # 修改这里，以便传递错误消息

    def __init__(self, array):
        super().__init__()
        self.array = array

    def run(self):
        try:
            table_engine = PPStructure(show_log=True, image_orientation=True)
            result = table_engine(self.array)
            self.recognition_complete.emit(result)
        except Exception as e:
            logger.error(f"表格识别失败: {e}")
            self.recognition_failed.emit(str(e))  # 传递错误消息
