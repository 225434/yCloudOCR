from python.controller.edit_controller import EditController
from python.controller.file_controller import FileController
from python.controller.recongnition_controller import RecognitionController
from python.controller.shot_controller import ShotController
from python.util.image_util import ImageUtil
from python.util.ui_util import UiUtil


class MainController:

    image_loaded = False

    def __init__(self, main_window):
        self.main_window = main_window
        self.ui_tool = UiUtil()
        self.image_util = ImageUtil()

        self.file_menu_manager = FileController(self.main_window)
        self.edit_menu_manager = EditController(self.main_window)
        self.screenshot_menu_manager = ShotController(self.main_window)
        self.recognition_menu_manager = RecognitionController(self.main_window)

        self.ui_tool.set_menu_enabled(self.edit_menu_manager.edit_menu, False)
        self.ui_tool.set_menu_enabled(self.screenshot_menu_manager.screenshot_menu, False)
        self.ui_tool.set_menu_enabled(self.recognition_menu_manager.recognition_menu, False)

        self.edit_menu_manager.edit_menu.aboutToShow.connect(self.editMenuClicked)
        self.screenshot_menu_manager.screenshot_menu.aboutToShow.connect(self.screenshotMenuClicked)
        self.recognition_menu_manager.recognition_menu.aboutToShow.connect(self.recognitionMenuClicked)

    def editMenuClicked(self):
        if self.file_menu_manager.is_image_loaded():
            self.ui_tool.set_menu_enabled(self.edit_menu_manager.edit_menu, True)

    def screenshotMenuClicked(self):
        if self.file_menu_manager.is_image_loaded():
            self.ui_tool.set_menu_enabled(self.screenshot_menu_manager.screenshot_menu, True)

    def recognitionMenuClicked(self):
        if self.file_menu_manager.is_image_loaded():
            self.ui_tool.set_menu_enabled(self.recognition_menu_manager.recognition_menu, True)
        if self.screenshot_menu_manager.is_result_image_loaded():
            self.recognition_menu_manager.set_image(self.image_util.qimage_to_array(
                self.ui_tool.get_qimage_from_result_image_view(self.main_window)))
        else:
            self.recognition_menu_manager.set_image(self.image_util.qimage_to_array(
                self.ui_tool.get_qimage_from_image_view(self.main_window)))
