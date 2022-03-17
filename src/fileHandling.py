# Defines methods to handle files: EXPORT, OPEN, SAVE

# OPEN
# void -> list of expression strings
# def openFile():
#     result = []
#     try:
#         with open('expr.logicshark', 'r') as f:
#             line = f.readline()
#             while line != '':
#                 result.append(line.rstrip())
#                 line = f.readline()
#
#             return result
#
#     # File does not exist
#     except FileNotFoundError:
#         return []
#
# # SAVE
# # list of expression strings -> void
# def saveFile(inputList):
#     with open('expr.logicshark', 'w') as f:
#         for i in inputList:
#             f.write(str(i) + '\n')
from PySide6.QtWidgets import QFileDialog


class FileHandling(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'File Handling'
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
        self.fileReader()

    #Writing to file
    def fileReader(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Files", "", "Expression Files (*.logicshark)")
        self._fileReader(fileName)

    def _fileReader(self, filename):
        try:
            with open(filename, 'r') as f:
                line = f.readline()
                result = []

                while line != '':
                    result.append(line.rstrip())
                    line = f.readline()

                print("READ: \n")
                for i in range(len(result)):
                    print(i, result[i])
        except FileNotFoundError:
            print("FUCK")


    def fileWriter(self):
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save File', 'default.logicshark', "Expression Files (*.logicshark)")
        print("SAVED: ", fileName)
        self._fileWriter(fileName)

    def _fileWriter(self, filename):
        try:
            lst = ['~A & (B & C)' for _ in range(16)]
            with open(filename, 'w') as f:
                for i in lst:
                    f.write(str(i) + '\n')
        except FileNotFoundError:
            print("SHIT")
