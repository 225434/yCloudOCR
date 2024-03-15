from datetime import datetime

import cv2
import numpy as np
from PyQt5.QtGui import QImage


class ImageUtil:

    @staticmethod
    def get_qimage_from_path(image_path):
        # 加载图像，并检查是否加载成功
        qimage = QImage(image_path)
        if qimage.isNull():
            raise ValueError(f"无法加载图像：{image_path}")
        return qimage

    @staticmethod
    def open_array(image_path):
        # 使用cv2读取图像，并确保它读取成功
        image_array = cv2.imread(image_path)
        if image_array is None:
            raise ValueError(f"无法加载图像：{image_path}")
        # 将BGR转换为RGB
        array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        return array

    @staticmethod
    def qimage_to_array(qimage):
        # 确保 QImage 是 32位RGB格式
        qimage = qimage.convertToFormat(QImage.Format_RGB32)
        width = qimage.width()
        height = qimage.height()
        ptr = qimage.bits()
        # 确保内存大小正确设置
        ptr.setsize(height * width * 4)
        # 创建一个相应的numpy数组视图
        array = np.frombuffer(ptr, dtype=np.uint8).reshape((height, width, 4))
        # 去除Alpha通道
        array_rgb = array[:, :, :3]

        # 转换为与cv2.imread()相同类型的数组
        array_cv2 = cv2.cvtColor(array_rgb, cv2.COLOR_RGB2BGR)

        return array_cv2

    @staticmethod
    def array_to_qimage(array):
        # 确保numpy数组是连续的，如果不是则复制为连续数组
        if not array.flags['C_CONTIGUOUS']:
            array = np.ascontiguousarray(array)

        if array.ndim == 2:
            h, w = array.shape
            return QImage(array.data, w, h, w, QImage.Format_Grayscale8)
        elif array.ndim == 3:
            h, w, ch = array.shape
            if ch == 3:
                # 确保数据类型正确
                if array.dtype != np.uint8:
                    raise ValueError("数组类型必须是np.uint8")
                return QImage(array.data, w, h, 3 * w, QImage.Format_RGB888)
            elif ch == 4:
                # 确保数据类型正确
                if array.dtype != np.uint8:
                    raise ValueError("数组类型必须是np.uint8")
                return QImage(array.data, w, h, 4 * w, QImage.Format_RGBA8888)
        else:
            raise ValueError("数组必须是2维灰度图或3/4维彩色图")

    @staticmethod
    def adjust_gamma(image, gamma=1.0):
        # 建立映射表
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255
                          for i in np.arange(0, 256)]).astype("uint8")
        # 应用伽马校正
        return cv2.LUT(image, table)

    @staticmethod
    def get_filename(tip):
        # 生成保存图像的文件名
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = f'saved_{tip}_image#{timestamp}.png'
        return filename
