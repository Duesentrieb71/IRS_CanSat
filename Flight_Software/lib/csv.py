
class CSV(object):
    def __init__(self, filename, header):
        self.filename = filename
        self.header = header
        self.file = open(filename, 'w')
        self.csv_write(header)

    def csv_write(self, line):
        for i in line:
            self.file.write(str(i) + ';')
        self.file.write('\n')

    def close(self):
        self.file.close()