#!/usr/bin/python

import subprocess
import sys
from file import *
from font import *
from glyph import *


class Otf2h:

	def __init__(self, font_name, font_size, ascii_only=False):
		self.asciiOnly = ascii_only
		self.fontName = font_name
		self.resolution = 112  # dpi
		self.fontSize = font_size

		self.__bdf_file = File(self.fontName, 'bdf')
		self.__header_file = File(self.fontName, 'h')

		self.gen_bdf_font()
		font = self.get_fmt_font()
		for g in font.glyphs:
			print(g)

	@staticmethod
	def run_bash_cmd(cmd):
		try:
			subprocess.check_call(cmd, shell=True)
		except Exception as e:
			print(e)

	@staticmethod
	def check_bash_cmd(cmd):
		try:
			subprocess.check_output(cmd, shell=True)
		except subprocess.CalledProcessError as grepexc:
			return False
		return True

	def read_cmd(self, cmd='', ret_values=False, ignore_command='COMMENT', ignore_any_command=False):
		__line = self.__bdf_file.read_line()

		print('line: ' + __line)

		if ignore_any_command:
			return

		while __line[:len(ignore_command)] == ignore_command:
			__line = self.__bdf_file.read_line()

		if __line[:len(cmd)] != cmd:
			raise Exception
		if ret_values:
			__output = []
			__tempValue = ''
			for c in __line[len(cmd)+1:]:
				if c == ' ' or c == '\n':
					__output.append(__tempValue)
					__tempValue = ''
				else:
					__tempValue = __tempValue + c
			return tuple(__output)

	def read_data(self):
		data = self.__bdf_file.read_line()
		data_fmt = 0x00
		number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'f', 'A', 'B', 'C', 'D', 'E',
		          'F']
		for i in range(0, int(len(data)/2), 2):
			if (data[i] not in number) or (data[i+1] not in number):
				raise Exception
			data_fmt |= int(data, 16) << (0xFF << int(i/2))

		return data_fmt

	def read_glyph_bitmap(self, glyph_width, glyph_height):
		bit = 0
		data = 0
		bytes_per_line = int((glyph_width - 1) / 8) + 1
		n = glyph_height * bytes_per_line
		data_array = [0x00] * n

		for i in range(0, n):
			last_bit = bit

			j = i % bytes_per_line
			if j == 0:
				data = self.read_data()

			byte = (data & (0xFF << j)) >> j
			data_array[i] |= byte << bit

			bit = (last_bit + glyph_width) % 8

		return data_array

	def gen_bdf_font(self):
		self.run_bash_cmd('sudo chmod 777 otf2bdf/mkinstalldirs')
		self.run_bash_cmd('sudo chmod 777 otf2bdf/configure')
		self.run_bash_cmd('otf2bdf/configure')
		self.run_bash_cmd('cd otf2bdf && sudo make install')
		self.run_bash_cmd('otf2bdf/otf2bdf -r ' + str(self.resolution) + ' -p ' + str(self.fontSize) + ' -o '
						  + self.fontName + '.bdf ' + self.fontName + '.ttf')

	def get_fmt_font(self):
		__bounding_box = BoundingBox()
		__font = Font()

		# ***Header***
		# Line 1
		self.read_cmd('STARTFONT')
		# Line 2
		self.read_cmd('FONT')
		# Line 3
		__font.size, __font.x_resolution, __font.y_resolution = self.read_cmd('SIZE', ret_values=True)
		__font.size = int(__font.size)
		__font.x_resolution = int(__font.x_resolution)
		__font.y_resolution = int(__font.y_resolution)
		# Line 4
		__bounding_box.width, __bounding_box.height, __bounding_box.x, __bounding_box.y = self.read_cmd('FONTBOUNDINGBOX', ret_values=True)
		__bounding_box.width = int(__bounding_box.width)
		__bounding_box.height = int(__bounding_box.height)
		__bounding_box.x = int(__bounding_box.x)
		__bounding_box.y = int(__bounding_box.y)
		__font.glyph_bounding_box = __bounding_box

		# ***Properties***
		__amountOfProperties = self.read_cmd('STARTPROPERTIES', ret_values=True)
		for i in range(0, int(__amountOfProperties[0])):
			self.read_cmd(ignore_any_command=True)
		self.read_cmd('ENDPROPERTIES')

		# ***Glyphs***
		__amountOfGlyphs = self.read_cmd('CHARS', ret_values=True)
		__amountOfGlyphs = int(__amountOfGlyphs[0])

		if self.asciiOnly:
			__amountOfGlyphs = (0x7e - 0x20) + 1

		for i in range(0, __amountOfGlyphs):
			__glyph = Glyph()

			self.read_cmd('STARTCHAR')
			__glyph.set_char(int(self.read_cmd('ENCODING', ret_values=True)[0]))

			if i == 0:
				__font.first_glyph_value = __glyph.get_char_value()
			else:
				__font.last_glyph_value = __glyph.get_char_value()

			if self.asciiOnly:
				if __glyph.get_char_value() < 0x20 or __glyph.get_char_value() > 0x7e:
					raise Exception

			self.read_cmd('SWIDTH')
			self.read_cmd('DWIDTH')
			__glyph.width, __glyph.height, __glyph.x_offset, __glyph.y_offset = self.read_cmd('BBX', ret_values=True)
			__glyph.width = int(__glyph.width)
			__glyph.height = int(__glyph.height)
			__glyph.x_offset = int(__glyph.x_offset)
			__glyph.y_offset = int(__glyph.y_offset)

			__glyph.x_advance = __glyph.width

			# read bitmap
			self.read_cmd('BITMAP')
			__bitmap = self.read_glyph_bitmap(__glyph.width, __glyph.height)
			self.read_cmd('ENDCHAR')
			__font.add_glyph(__glyph, __bitmap)

		if self.asciiOnly:
			while self.__bdf_file.read_line() != 'ENDFONT\n':
				pass
		else:
			self.read_cmd('ENDFONT')

		return __font


otf2h = Otf2h(str(sys.argv[1]), sys.argv[2], False)
