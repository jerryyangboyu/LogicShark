from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile

class Stats:

	def __init__(self):

		readFile = QFile("UI\defualt.ui")
		readFile.open(QFile.ReadOnly)
		readFile.close()

		self.ui = QUiLoader().load(readFile)

		self.ui.pushButton.clicked.connect(self.handleCalc)

	def handleCalc(self):
		print ("FUCKYOUWORLD")

app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()
