from pathlib import Path

from python.service.file_service import FileService
from python.util.drop_dialog import DropDialog
from python.util.image_util import ImageUtil
from python.util.signal_control import SignalControl
from python.util.ui_util import UiUtil

SAVED_DIR = 'D:/Code/Python/OCR_Pro/saved'


class FileController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.file_menu = main_window.menubar.addMenu("文件")
        self.ui_tool = UiUtil()
        self.image_tool = ImageUtil()
        self.signal = SignalControl()
        self.image_loaded = False
        self.ui_tool.add_action(self.main_window, self.file_menu, "打开图片", self.open_image)
        self.recent_projects_menu = self.file_menu.addMenu("最近的项目")
        self.file_service = FileService(main_window, self.recent_projects_menu)
        self.setup_file_menu_actions()

    def setup_file_menu_actions(self):
        self.file_menu.addSeparator()
        self.ui_tool.add_action(self.main_window, self.file_menu, "打开存储目录", self.open_dir)
        self.file_menu.addSeparator()
        self.ui_tool.add_action(self.main_window, self.file_menu, "拖拽打开文件", self.drop_open_file)
        self.update_recent_projects_menu()

    def open_image(self):
        image = self.file_service.open_image()
        if image:
            self.ui_tool.load_image(image, self.main_window.image_scene, self.main_window.image_view)
        self.image_loaded = True

    def update_recent_projects_menu(self):
        self.file_service.update_recent_projects_menu()

    def open_dir(self):
        self.ui_tool.open_folder_dialog(SAVED_DIR)

    def drop_open_file(self):
        dialog = DropDialog(self.open_image_from_path, self.main_window)
        dialog.exec_()
        self.image_loaded = True

    def open_image_from_path(self, file_path):
        # 使用已有的open_image方法打开图片，或者直接处理文件路径
        qimage = self.image_tool.get_qimage_from_path(file_path)
        self.file_service.update_recently_opened_files(Path(file_path), qimage)
        self.file_service.update_recent_projects_menu()
        self.ui_tool.load_image(qimage, self.main_window.image_scene, self.main_window.image_view)

    def is_image_loaded(self):
        return self.image_loaded
