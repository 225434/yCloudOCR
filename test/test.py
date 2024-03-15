import cv2
import numpy as np

# 读取图像
image = cv2.imread('E:/temp/table.png')
# 转换为灰度图
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 使用Canny边缘检测
edges = cv2.Canny(gray, 50, 150, apertureSize=7)

# 使用HoughLinesP进行线检测
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=200, maxLineGap=5)

# 将检测到的线绘制在原图上
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# 显示带有线条的图像
cv2.imshow('Image with Lines', image)
cv2.waitKey(0)
cv2.destroyAllWindows()