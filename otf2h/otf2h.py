#!/usr/bin/python

import subprocess
import sys

class Otf2h:

    def __init__(self, fontName, fontSize, asciiOnly = False):
        self.asciiOnly = asciiOnly
        self.fontName = fontName
        self.resolution = 112 #dpi
        self.fontSize = fontSize

        self.__bdfIsOpen = False
        self.__hIsOpen = False

        self.genBDFFont()
        self.genHFont()

    def run_bash_cmd(self, cmd):
        try:
            subprocess.check_call(cmd, shell=True)
        except Exception as e:
            print e

    def check_bash_cmd(self, cmd):
        try:
            subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as grepexc:
            return False
        return True

    def genBDFFont(self):
        self.run_bash_cmd('sudo chmod 777 mkinstalldirs')
        self.run_bash_cmd('./configure')
        self.run_bash_cmd('sudo make install')
        self.run_bash_cmd('./otf2bdf -r ' + str(self.resolution) + ' -p ' + str(self.fontSize) + ' -o ' + self.fontName[:-4] + '.bdf ' + self.fontName)

    def genHFont(self):
        # Header
        ## Line 1
        __bdfVersion = self.read_cmd('STARTFONT', retValues=True)
        __bdfVersion = float(__bdfVersion[0])
        ## Line 2
        self.read_cmd('FONT')
        ## Line 3
        self.read_cmd('SIZE')
        ## Line 4
        __width, __height, __xStart, __yStart = self.read_cmd('FONTBOUNDINGBOX', retValues=True)
        __width = int(__width)
        __height = int(__height)
        __xStart = int(__xStart)
        __yStart = int(__yStart)

        # Properties
        __amountOfProperties = self.read_cmd('STARTPROPERTIES', retValues=True)
        for i in xrange(0, __amountOfProperties+1):
            self.read_cmd(ignoreAnyCommand=True)

        # Glyphs
        if self.asciiOnly:
            __amountOfGlyphs = (16*6)-1
        else:
            __amountOfGlyphs = self.read_cmd('CHARS', retValues=True)
            __amountOfGlyphs = int(__amountOfGlyphs)

        for i in xrange(0, __amountOfGlyphs):
            if self.asciiOnly:
                pass
            else:
                __glyphValue = self.read_cmd('STARTCHAR', retValues=True)

        pass

    def read_cmd(self, cmd = '', retValues = False, ignoreCommand = 'COMMENT', ignoreAnyCommand = False):
        while(__line[:len(ignoreCommand)] == ignoreCommand):
            __line = self.read_line()

        if ignoreAnyCommand:
            return

        if __line[:len(cmd)] != cmd:
            raise Exception
        if retValues:
            __output = []
            __tempValue = ''
            for c in xrange(len(cmd)+1, len(__line)):
                if (c == ' ' or c == '\n'):
                    __output.append(__tempValue)
                    __tempValue = ''
                else:
                    __tempValue = __tempValue + c
            return tuple(__output)

    def read_line(self):
        pass


otf2h = Otf2h(str(sys.argv[0]), sys.argv[1])
