

class Glyph:
    def __init__(self, bitmap_pos=0, width=0, height=0, x_advance=0, x_offset=0, y_offset=0, char=' '):
        self.bitmap_pos = bitmap_pos
        self.x_advance = x_advance
        self.width = width
        self.height = height
        self.x_offset = x_offset
        self.y_offset = y_offset

        self.__char = char
        self.__char_value = ord(self.char)

    def __str__(self):
        return '[{}({})|{},{},{},{},{},{}]'.format(self.__char, hex(self.__char_value), self.bitmap_pos, self.width,
                                                   self.height, self.x_advance, self.x_offset, self.y_offset)

    def set_char(self, char_value):
        self.__char_value = char_value
        self.__char = chr(char_value)

