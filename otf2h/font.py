

class BoundingBox:
    def __init__(self, x=0, y=0, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        pass

    def __str__(self):
        return '[({}, {}), ({}, {})]'.format(self.x, self.y, self.width, self.height)


class Font:
    def __init__(self, bitmap=[], glyphs=[], first_glyph_value=0x20, last_glyph_value=0x7e, y_advance=0, size=0, x_resolution=0,
                 y_resolution=0, glyph_bb_x=0, glyph_bb_y=0, glyph_bb_width=0, glyph_bb_height=0):
        self.bitmap = bitmap
        self.glyphs = glyphs
        self.first_glyph_value = first_glyph_value
        self.last_glyph_value = last_glyph_value
        self.y_advance = y_advance
        self.size = size
        self.x_resolution = x_resolution
        self.y_resolution = y_resolution
        self.glyph_bounding_box = BoundingBox(glyph_bb_x, glyph_bb_y, glyph_bb_width, glyph_bb_height)

        self.bitmap_cursor = 0

    def __str__(self):
        return '[{}]'.format()

    def set_y_advance(self, y_advance):
        self.y_advance = y_advance
        if self.y_advance == 0:
            self.y_advance = self.glyph_bounding_box.height

    def add_glyph(self, glyph_, bitmap):
        glyph_.bitmap_pos = self.bitmap_cursor
        for byte in bitmap:
            self.bitmap_cursor = self.bitmap_cursor + 1
            self.bitmap.append(byte)

        self.glyphs.append(glyph_)

