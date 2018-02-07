import cv2
import numpy as np
from __builtin__ import unichr
from otf2h import otf2h

DISPLAY_WIDTH = 296
DISPLAY_HEIGHT = 128
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FONT = otf2h.Otf2h('arial', 12)
FONT = FONT.font


def write_pixel(img_, x, y, color):
	img_[x, y] = color
	return img_


def write_char(img_, char, x, y):
	char_value = unichr(char)
	glyph = FONT.glyphs[char_value-0x20]

	top_left = ()

	return img_


def write_string(img_, string_, x, y):
	for c in string_:
		write_char(img_, c, x, y)
	return img_


def clear_img():
	return np.zeros((DISPLAY_WIDTH, DISPLAY_HEIGHT, 3), np.uint8)

img = clear_img()
img = write_string(img, 'Matheus Tenorio', 10, 10)

while True:
	cv2.imshow('img', img)

	cv2.waitKey(1)

