from UIElements.WindowController import *
from ib_insync.ib import IB, util
import sys


if __name__ == "__main__":
    util.patchAsyncio()
    util.useQt("PyQt6", 0.03)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = WindowController(None)
    MainWindow.show()
    IB.run()
    sys.exit(app.exec())

