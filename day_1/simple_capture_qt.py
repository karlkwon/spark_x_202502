import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage,QPixmap
from PyQt5 import uic
from PyQt5.QtCore import *
import cv2,imutils

# import rclpy
# from rclpy.node import Node
# from sensor_msgs.msg import CompressedImage
import numpy as np

import queue
import time
from threading import Thread


form_class = uic.loadUiType("simple_qt_ros.ui")[0]

class WindowClass(QMainWindow, form_class):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		self.btn_1.clicked.connect(self.button1Function)
		self.btn_2.clicked.connect(self.button2Function)

		# self.isClosed = False

		# OpenCV 비디오 캡처 객체 생성 (카메라 0번 장치 사용)
		self.cap = cv2.VideoCapture(2, cv2.CAP_V4L2)
		self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
		self.cap.set(cv2.CAP_PROP_FPS, 25)
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

		print(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

		self.timer = QTimer(self)
		self.timer.start(100)
		self.timer.timeout.connect(self.showImage)

		self.frame = None
		self.file_idx = 0

	def button1Function(self):
		print("btn_1 clicked")

		img_path = 'images/saved_image_%03d.jpg' % self.file_idx
		cv2.imwrite(img_path, self.frame)

		self.file_idx += 1

	def button2Function(self):
		print("btn_2 clicked")

	def editAddFunction(self, text):
		self.edit_1.append(text)

	def showImage(self):
		ret, self.frame = self.cap.read()

		if ret:
			image = self.cvimage_to_label(self.frame)
			self.label_1.setPixmap(QPixmap.fromImage(image))

	def cvimage_to_label(self, image):
		image = imutils.resize(image,width = 640)
		image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
		image = QImage(image,
			image.shape[1],
			image.shape[0],
			QImage.Format_RGB888)

		return image

	def closeEvent(self, event):
		print("closeEvent")


if __name__ == "__main__":
	app = QApplication(sys.argv)
	myWindow = WindowClass()

	myWindow.show()
	app.exec_()
