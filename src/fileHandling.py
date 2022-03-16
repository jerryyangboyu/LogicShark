# Defines methods to handle files: EXPORT, OPEN, SAVE
from Main import MainWindow

# OPEN
# void -> list of expression strings
def openFile():
    result = []
    try:
        with open('expr.logicshark', 'r') as f:
            line = f.readline()
            while line != '':
                result.append(line.rstrip())
                line = f.readline()

            return result

    # File does not exist
    except FileNotFoundError:
        return []

# SAVE
# list of expression strings -> void
def saveFile(inputList):
    with open('expr.logicshark', 'w') as f:
        for i in inputList:
            f.write(str(i) + '\n')


# TODO: EXPORT:
# Export QGraphicsScene as an image
def exportGraph():
    pass