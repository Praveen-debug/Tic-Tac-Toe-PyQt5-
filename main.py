from PyQt5 import QtCore, QtGui, QtWidgets
import Game_Code as Game
import random
from math import floor
from PyQt5.QtWidgets import QMessageBox
import sys

# User = X, AI = 0

if __name__ == "__main__":
	GameApp = QtWidgets.QApplication(sys.argv)
	gameMW = QtWidgets.QMainWindow()
	gameUI = Game.Ui_MainWindow()
	gameUI.setupUi(gameMW)
	gameMW.show()
	sys.exit(GameApp.exec_())