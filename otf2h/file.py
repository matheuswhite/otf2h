

class File:
    def __init__(self, file_name, type_, lazy=True):
        self.file_name = file_name
        self.type = type_

        self.__file = None
        if not lazy:
            self.open()

    def __str__(self):
        return '[{}.{}, open = {}]'.format(self.file_name, self.type, self.__file is not None)

    def open(self):
        self.__file = open(self.file_name + '.' + self.type, 'r')

    def close(self):
        if self.__file is not None:
            self.__file.close()
            self.__file = None

    def read_line(self):
        if self.__file is None:
            self.open()
        return self.__file.readline()

