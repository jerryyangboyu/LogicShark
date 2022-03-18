# Defines methods to handle files: EXPORT, OPEN, SAVE
import sys
from typing import List, Tuple

from PySide6.QtWidgets import QFileDialog, QWidget, QApplication
import glob


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

    # Writing to file
    def getResult(self):
        fileName, _ = QFileDialog.getOpenFileName \
            (self, "Open Files", "", "Expression Files (*.logicshark)")
        return self._fileReader(fileName)

    def _fileReader(self, filename) -> Tuple[List, List]:
        try:
            with open(filename, 'r') as f:
                line = f.readline()
                labels = []
                exprs = []

                while line != '':
                    arr = line.rstrip().split("=")
                    labels.append(arr[0])
                    exprs.append(arr[1])
                    line = f.readline()

                return labels, exprs

        except FileNotFoundError:
            return [], []


class FileWriting(QWidget):
    def __init__(self, labelList, exprList):
        super().__init__()
        self.title = 'File Handling'
        self.toBeSaved = [labelList, exprList]
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
                for i in range(len(self.toBeSaved[0])):
                    f.write(self.toBeSaved[0][i] + "=" + self.toBeSaved[1][i] + "\n")
        except FileNotFoundError:
            pass


def launchReader():
    return FileReading().getResult()


def launchWriter(labelList, exprList):
    ex = FileWriting(labelList, exprList)


def readAllFileWithExtension():
    r = glob.glob('*.logicshark', recursive=True)
    print(r)
