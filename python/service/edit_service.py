import cv2
import numpy as np

from python.util.image_util import ImageUtil
from python.util.ui_util import UiUtil


class EditService:

    def __init__(self):
        self.ui_tool = UiUtil()
        self.image_tool = ImageUtil()
        self.processed_image_cache = {}

    @staticmethod
    def adjust_gamma(image, gamma=1.0):
        # 建立映射表
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")
        # 应用伽马校正
        return cv2.LUT(image, table)

    def enhance_image(self, image_array):
        self.processed_image_cache['image_array_copy'] = image_array
        if 'enhanced' not in self.processed_image_cache:
            gamma = 1.5
            image_gamma_corrected = EditService.adjust_gamma(image_array, gamma=gamma)  # 注意这里的静态方法调用
            self.processed_image_cache['enhanced'] = image_gamma_corrected
        return self.processed_image_cache['enhanced']

    def convert_to_grayscale(self, image_array):
        self.processed_image_cache['image_array_copy'] = image_array
        if 'grayscale' not in self.processed_image_cache:
            gray_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
            self.processed_image_cache['grayscale'] = gray_image
        return self.processed_image_cache['grayscale']

    def adaptive_thresholding(self, image_array):
        self.processed_image_cache['image_array_copy'] = image_array
        if 'thresholded' not in self.processed_image_cache:
            # 将图像转换为灰度图
            gray_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)  # 假设输入的是BGR图像

            # 使用自适应阈值方法
            binary_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                                 cv2.THRESH_BINARY, 11, 2)
            self.processed_image_cache['thresholded'] = binary_image
        return self.processed_image_cache['thresholded']

    def reset_image(self):
        if 'image_array_copy' not in self.processed_image_cache:
            self.processed_image_cache['image_array_copy'] = None
        return self.processed_image_cache['image_array_copy']

    def table_enhance(self, array):
        self.processed_image_cache['image_array_copy'] = array
        if 'table_enhance' not in self.processed_image_cache:
            gray = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
            # 使用Canny边缘检测
            edges = cv2.Canny(gray, 50, 150, apertureSize=7)
            # 使用HoughLinesP进行线检测
            lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=200, maxLineGap=5)
            # 将检测到的线绘制在原图上
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(array, (x1, y1), (x2, y2), (0, 255, 0), 2)
            self.processed_image_cache['table_enhance'] = array
        return self.processed_image_cache['table_enhance']
