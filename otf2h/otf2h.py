#!/usr/bin/python

import subprocess
import sys
from otf2h import file
from otf2h import font
from otf2h import glyph


class Otf2h:

    def __init__(self, font_name, font_size, ascii_only = False):
        self.asciiOnly = ascii_only
        self.fontName = font_name
        self.resolution = 112  # dpi
        self.fontSize = font_size

        self.__bdf_file = file.File(self.fontName, 'bdf')
        self.__header_file = file.File(self.fontName, 'h')

        self.gen_bdf_font()
        self.gen_h_font()

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

        if ignore_any_command:
            return

        while __line[:len(ignore_command)] == ignore_command:
            __line = self.__bdf_file.read_line()

        if __line[:len(cmd)] != cmd and cmd != '$only_data$':
            raise Exception
        if ret_values:
            __output = []
            __tempValue = ''
            for c in range(len(cmd)+1, len(__line)):
                if c == ' ' or c == '\n':
                    __output.append(__tempValue)
                    __tempValue = ''
                else:
                    __tempValue = __tempValue + c
            return tuple(__output)

    def gen_bdf_font(self):
        self.run_bash_cmd('sudo chmod 777 mkinstalldirs')
        self.run_bash_cmd('./configure')
        self.run_bash_cmd('sudo make install')
        self.run_bash_cmd('./otf2bdf -r ' + str(self.resolution) + ' -p ' + str(self.fontSize) + ' -o ' + self.fontName[:-4] + '.bdf ' + self.fontName)

    def gen_h_font(self):
        __font = font.Font()
        __bounding_box = font.BoundingBox()
        __glyph = glyph.Glyph()

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
        for i in range(0, int(__amountOfProperties)):
            self.read_cmd(ignore_any_command=True)
        self.read_cmd('ENDPROPERTIES')

        # ***Glyphs***
        if self.asciiOnly:
            __amountOfGlyphs = (0x7e - 0x20) + 1
        else:
            __amountOfGlyphs = self.read_cmd('CHARS', ret_values=True)
            __amountOfGlyphs = int(__amountOfGlyphs)

        for i in range(0, __amountOfGlyphs):
            self.read_cmd('STARTCHAR')
            __glyph.set_char(self.read_cmd('ENCODING', ret_values=True))

            if i == 0:
                __font.first_glyph_value = __glyph.__char_value
            else:
                __font.last_glyph_value = __glyph.__char_value

            if self.asciiOnly:
                if __glyph.__char_value < 0x20 or __glyph.__char_value > 0x7e:
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
            __bitmap = []
            while 1:
                __data = self.__bdf_file.read_line()
                if __data == 'ENDCHAR':
                    break
                __bitmap.append(int(__data))

            __font.add_glyph(__glyph, __bitmap)

        self.read_cmd('ENDFONT')


otf2h = Otf2h(str(sys.argv[1]), sys.argv[2])
