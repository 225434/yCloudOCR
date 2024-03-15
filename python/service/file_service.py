from pathlib import Path

from PyQt5.QtWidgets import (
    QAction, QFileDialog
)

from python.util.image_util import ImageUtil
from python.util.ui_util import UiUtil

IMAGE_FILTERS = "Images (*.png *.jpg *.bmp)"
MAX_RECENT_FILES = 10


class FileService:
    def __init__(self, main_window, recent_projects_menu):
        self.main_window = main_window
        self.file_dialog = QFileDialog()
        self.recently_opened_files = {}
        self.ui_tool = UiUtil()
        self.image_tool = ImageUtil()
        self.recent_projects_menu = recent_projects_menu

    def open_image(self):
        # 使用Pathlib处理路径
        file_path, _ = self.file_dialog.getOpenFileName(self.main_window,
                                                        "Open Image File",
                                                        "resources/static/images",
                                                        IMAGE_FILTERS)
        if file_path:
            qimage = self.image_tool.get_qimage_from_path(file_path)
            self.update_recently_opened_files(Path(file_path), qimage)
            self.update_recent_projects_menu()
            self.ui_tool.load_image(qimage, self.main_window.image_scene, self.main_window.image_view)

    def update_recently_opened_files(self, file_path, qimage):
        if file_path not in self.recently_opened_files:
            if len(self.recently_opened_files) >= MAX_RECENT_FILES:
                oldest_key = next(iter(self.recently_opened_files))
                del self.recently_opened_files[oldest_key]
            self.recently_opened_files[file_path] = qimage

    def update_recent_projects_menu(self):
        self.recent_projects_menu.clear()
        if not self.recently_opened_files:
            self.recent_projects_menu.addAction(self.create_action("无项目", enabled=False))
        else:
            for path, qimage in reversed(self.recently_opened_files.items()):
                self.recent_projects_menu.addAction(self.create_action(Path(path).name, qimage))

    def create_action(self, text, qimage=None, enabled=True):
        action = QAction(text, self.main_window)
        action.setEnabled(enabled)
        if qimage:
            action.triggered.connect(lambda: self.ui_tool.load_image(qimage,
                                                                     self.main_window.image_scene,
                                                                     self.main_window.image_view))
        return action
