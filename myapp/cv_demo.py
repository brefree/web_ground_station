# _*_ coding: utf-8 _*_
__author__ = 'Ray'
__date__ = '2018/11/6 11:01'

# 导入cv模块
import cv2 as cv

# 读取图像，支持 bmp、jpg、png、tiff 等常用格式
img = cv.imread("../static/img/uav.jpg")
# 创建窗口并显示图像
cv.namedWindow("Image")
cv.imshow("Image", img)
cv.waitKey(0)
# 释放窗口
cv2.destroyAllWindows()
