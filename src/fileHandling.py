# Defines methods to handle files: EXPORT, OPEN, SAVE
import sys
from PySide6.QtWidgets import QFileDialog, QWidget, QApplication

class FileReading(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'File Handling'
        self.result = []
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Method to run
        self.fileReader()

    #Writing to file
    def fileReader(self):
        fileName, _ = QFileDialog.getOpenFileName \
            (self, "Open Files", "", "Expression Files (*.logicshark)")
        resultList = self._fileReader(fileName)
        self.result = resultList

    def _fileReader(self, filename):
        try:
            with open(filename, 'r') as f:
                line = f.readline()
                result = []

                while line != '':
                    result.append(line.rstrip())
                    line = f.readline()

                return result

        except FileNotFoundError:
            return []

class FileWriting(QWidget):
    def __init__(self, exprList):
        super().__init__()
        self.title = 'File Handling'
        self.exprList = exprList
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Method to run
        self.fileWriter()


    def fileWriter(self):
        fileName, _ = QFileDialog.getSaveFileName \
            (self, 'Save File', 'default.logicshark', "Expression Files (*.logicshark)")
        print("SAVED: ", fileName)
        self._fileWriter(fileName)

    def _fileWriter(self, filename):
        try:
            with open(filename, 'w') as f:
                for i in self.exprList:
                    f.write(str(i) + '\n')
        except FileNotFoundError:
            pass

def launchReader():
    ex = FileReading()
    return ex.result

def launchWriter(exprList):
    ex = FileWriting(exprList)


