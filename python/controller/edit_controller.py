import cv2
import numpy as np

from python.service.edit_service import EditService
from python.util.image_util import ImageUtil
from python.util.signal_control import SignalControl
from python.util.ui_util import UiUtil


class EditController:
    def __init__(self, main_window):
        self.main_window = main_window  # 保存对主窗口的引用
        self.edit_menu = main_window.menubar.addMenu("编辑")

        self.ui_tool = UiUtil()
        self.image_util = ImageUtil()
        self.edit_service = EditService()
        self.image_array = self.image_util.qimage_to_array(self.ui_tool.get_qimage_from_image_view(main_window))
        self.image_array_copy = self.image_array

        self.setup_edit_menu_actions()

    def setup_edit_menu_actions(self):
        # 这里添加所有编辑菜单项self.current
        actions = [
            ("图像增强", self.enhance),
            ("表格增强", self.table_enhance),
            ("灰度化", self.grayscale),
            ("二值化", self.thresholding),
            ("倾斜校正", self.correction),
            ("Separator", None),
            ("顺时针旋转", self.rotate_clockwise),
            ("逆时针旋转", self.rotate_counterclockwise),
            ("Separator", None),
            ("重置图片", self.reset)
        ]
        for action_text, callback in actions:
            if action_text == "Separator":
                self.edit_menu.addSeparator()
            else:
                self.ui_tool.add_action(self.main_window, self.edit_menu, action_text, callback)

    def enhance(self):
        image_array = self.image_util.qimage_to_array(self.ui_tool.get_qimage_from_image_view(self.main_window))
        self.ui_tool.load_image(self.image_util.array_to_qimage(self.edit_service.enhance_image(image_array)),
                                self.main_window.image_scene, self.main_window.image_view)

    def table_enhance(self):
        image_array = self.image_util.qimage_to_array(self.ui_tool.get_qimage_from_image_view(self.main_window))
        self.ui_tool.load_image(self.image_util.array_to_qimage(self.edit_service.table_enhance(image_array)),
                                self.main_window.image_scene, self.main_window.image_view)

    def grayscale(self):
        image_array = self.image_util.qimage_to_array(self.ui_tool.get_qimage_from_image_view(self.main_window))
        self.ui_tool.load_image(self.image_util.array_to_qimage(
            self.edit_service.convert_to_grayscale(image_array)),
                                self.main_window.image_scene, self.main_window.image_view)

    def thresholding(self):
        image_array = self.image_util.qimage_to_array(self.ui_tool.get_qimage_from_image_view(self.main_window))
        self.ui_tool.load_image(self.image_util.array_to_qimage(
            self.edit_service.adaptive_thresholding(image_array)),
                                self.main_window.image_scene, self.main_window.image_view)

    def reset(self):
        self.ui_tool.load_image(self.image_util.array_to_qimage(
            self.edit_service.reset_image()),
            self.main_window.image_scene, self.main_window.image_view)

    def correction(self):
        # 将QImage转换为数组以便处理
        image_array = self.image_util.qimage_to_array(self.ui_tool.get_qimage_from_image_view(self.main_window))
        # 转换为灰度图像
        gray_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        # 使用Canny算子获取边缘
        edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)
        # 使用霍夫变换检测直线
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

        if lines is not None:
            # 计算所有检测到的线的平均倾斜角度
            angles = []
            for rho, theta in lines[:, 0]:
                angles.append(theta)

            # 计算所有角度的平均值
            average_angle = np.rad2deg(np.mean(angles))
            # 转换角度，使其适用于旋转
            angle = average_angle - 90

            # 获取图像的中心点
            image_center = tuple(np.array(gray_image.shape[1::-1]) / 2)
            # 计算旋转矩阵
            rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
            # 执行仿射变换(旋转图像)
            corrected_image = cv2.warpAffine(image_array, rot_mat, gray_image.shape[1::-1], flags=cv2.INTER_LINEAR)

            # 将校正后的图像显示出来
            self.ui_tool.load_image(self.image_util.array_to_qimage(corrected_image),
                                    self.main_window.image_scene, self.main_window.image_view)

    def rotate_clockwise(self):
        image_array = self.image_util.qimage_to_array(self.ui_tool.get_qimage_from_image_view(self.main_window))
        # 对图像进行顺时针旋转90度
        rotated_image = cv2.rotate(image_array, cv2.ROTATE_90_CLOCKWISE)
        self.ui_tool.load_image(self.image_util.array_to_qimage(rotated_image),
                                self.main_window.image_scene, self.main_window.image_view)
        return rotated_image

    def rotate_counterclockwise(self):
        image_array = self.image_util.qimage_to_array(self.ui_tool.get_qimage_from_image_view(self.main_window))
        # 对图像进行逆时针旋转90度
        rotated_image = cv2.rotate(image_array, cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.ui_tool.load_image(self.image_util.array_to_qimage(rotated_image),
                                self.main_window.image_scene, self.main_window.image_view)
        return rotated_image
