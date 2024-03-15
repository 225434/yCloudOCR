from PyQt5.QtCore import QThread, pyqtSignal


class RecognitionThread(QThread):
    textRecognized = pyqtSignal(str)

    def __init__(self, image, recognition_service):
        super().__init__()
        self.image = image
        self.recognition_service = recognition_service

    def run(self):
        text = self.recognition_service.recognize_text(self.image)
        self.textRecognized.emit(text)
