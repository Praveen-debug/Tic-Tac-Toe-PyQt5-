from PyQt5 import QtCore, QtGui, QtWidgets
import random
from math import floor
from PyQt5.QtWidgets import QMessageBox
from functools import partial
import sys


# User = X, AI = 0

# Game Algorithm

class Game():
    # All possiable chances to win or loose the game
    Chances = [[0, 1, 2], [3, 4, 5], [6 , 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    # Value of each box in the game | 0 = undefined, X = User, O = AI
    boxMap = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # Current index of the patter following
    patternCurrentIndex = None
    # Curent Pattern
    pattern = None

    # Function to update if there is any change in the game boxes

    def updateBoxMap(self, index, value):
        self.boxMap[index] = value;

    # Function to check if the game is ended

    def checkOver(self):
            def userWin():
                for chance in self.Chances:
                    if self.boxMap[chance[0]] == "X" and self.boxMap[chance[1]] == "X" and self.boxMap[chance[2]] == "X":
                        return True
                    else:
                        continue;
                return False
            def aiWin():
                for chance in self.Chances:
                    if self.boxMap[chance[0]] == "O" and self.boxMap[chance[1]] == "O" and self.boxMap[chance[2]] == "O":
                        return True
                    else:
                        continue
                return False
            def draw():
                for i in range(9):
                    if self.boxMap[i] == 0:
                        return False
                return True
            if userWin() == True:
                return "Congrats You Won"
            elif aiWin() == True:
                return "Oops Ai Won"
            elif draw() == True:
                return "Game draw!!!"
            else:
                return False

    # Main function that interacts with the UI

    def main(self):
        if self.checkOver() == False:
            if self.Win() !=  False:
                result = self.Win()
                self.updateBoxMap(result, "O")
                return [result, True]
            elif self.Danger() != False:
                result = self.Danger()
                self.updateBoxMap(result, "O")
                return result
            elif self.pattern == None:
                if self.createPattern() != False:
                        pattern = self.createPattern()
                        patternCurrentIndex = 0
                        result = self.buildPattern()
                        self.updateBoxMap(result, "O")
                        return result
                else:
                    result = self.Prevent()
                    self.updateBoxMap(result, "O")
                    return result
            elif self.pattern != None:
                if self.checkPattern() != False:
                    result = self.buildPattern()
                    self.updateBoxMap(result, "O")
                    return result
                else:
                    self.pattern = None
                    self.patternCurrentIndex = 0
                    if self.createPattern() != False:
                        self.pattern = self.createPattern()
                        self.patternCurrentIndex = 0
                        result = self.buildPattern()
                        self.updateBoxMap(result, "O")
                        return result
                    else:
                        result = self.Prevent()
                        self.updateBoxMap(result, "O")
                        return result
        else:
            return self.checkOver()

    # Function that checks if the user is going to win the game

    def Danger(self):
        for chance in self.Chances:
            counter = 0;
            for index in chance:
                if self.boxMap[index] == "X":
                    counter += 1
                    continue
            if counter == 2:
                for i in chance:
                    if self.boxMap[i] == 0:
                        return i
            else:
                continue
        return False

    # Function that checks if AI is going to win the game

    def Win(self):
        for chance in self.Chances:
            counter = 0;
            for index in chance:
                if self.boxMap[index] == "O":
                    counter += 1
            if counter == 2:
                for i in chance:
                    if self.boxMap[i] == 0:
                        return i
            else:
                continue
        return False

    # Method which creates a pattern which can be used to win | return {a set or integers} as True, {False} is there is none 

    def createPattern(self):
        for chance in self.Chances:
            counter = 0;
            for index in chance:
                if self.boxMap[index] == 0:
                    counter += 1
                    continue
            if counter == 3:
                self.pattern = chance
                self.patternCurrentIndex = 0;
                return chance
            else:
                continue
        return False

    # Check if the pattern create by createPatter method is still useable | return True or False

    def checkPattern(self):
        for p in self.pattern:
            if self.boxMap[p] != 0 or self.boxMap[p] != "O":
                return False
        return True

    # return the the index of the next build block of the pattern
        
    def buildPattern(self):
        result =  self.pattern[self.patternCurrentIndex]
        self.patternCurrentIndex += 1
        return result

    def Prevent(self):
        for i in range(9):
            if self.boxMap[i] == 0:
                return i;


# Game Ui

class Ui_MainWindow(object):
    MainWindow = None
    counter = 1
    firstChoose = False
    boxes = []
    game = Game()

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(805, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Dice = QtWidgets.QPushButton(self.centralwidget)
        self.Dice.setGeometry(QtCore.QRect(230, 260, 311, 111))
        font = QtGui.QFont()
        font.setFamily("Lithos Pro Regular")
        font.setPointSize(22)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(10)
        self.Dice.setFont(font)
        self.Dice.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.MainWindow.setWindowTitle("Roll Dice")
        self.Dice.setStyleSheet("background: rgb(234, 234, 234);\n"
                                                                    "font: 87 22pt \"Lithos Pro Regular\";\n"
                                                                    "color: black;\n"
                                                                    "border-radius: 7px;\n"
                                                                    "font-size: 2rem;\n"
                                                                    "cursor: ;")
        self.Dice.setObjectName("Dice")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 160, 701, 71))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.Dice.clicked.connect(self.roll_dice)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def roll_dice(self):
        x = floor(random.uniform(0, 2))
        m = QMessageBox()
        m.setIcon(QMessageBox.Information)
        m.setStandardButtons(QMessageBox.Ok)
        if x == 1:
            self.firstChoose = True
            m.setWindowTitle("AI got it")
            m.setText("AI got the first play")
            m.setStyleSheet("color: red")
        else:
            m.setWindowTitle("You got it")
            m.setText("You got the first play")
            m.setStyleSheet("color: green")
        m.buttonClicked.connect(self.messageBoxClicked)
        y = m.exec_()

    def messageBoxClicked(self, element):
        if element.text().lower() == "ok":


            # Loading the Game UI


            self.Dice.deleteLater()
            self.label.deleteLater()

            self.centralwidget = QtWidgets.QWidget(self.MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.frame = QtWidgets.QFrame(self.centralwidget)
            self.frame.setGeometry(QtCore.QRect(160, 70, 511, 481))
            font = QtGui.QFont()
            font.setPointSize(48)
            self.frame.setFont(font)
            self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame.setObjectName("frame")
            self.MainWindow.setWindowTitle("Tic Tac Toe Game")


            # Function to add styles to them

            def add_style(element):
                font = QtGui.QFont()
                font.setPointSize(72)
                element.setFont(font)
                element.setStyleSheet("border: 2px solid black;\n")
                element.setObjectName(f'Box_{self.counter}')
                self.counter += 1

            # Creating boxes

            self.Box_1 = QtWidgets.QLabel(self.frame)
            self.Box_2 = QtWidgets.QLabel(self.frame)
            self.Box_3 = QtWidgets.QLabel(self.frame)
            self.Box_4 = QtWidgets.QLabel(self.frame)
            self.Box_5 = QtWidgets.QLabel(self.frame)
            self.Box_6 = QtWidgets.QLabel(self.frame)
            self.Box_7 = QtWidgets.QLabel(self.frame)
            self.Box_8 = QtWidgets.QLabel(self.frame)
            self.Box_9 = QtWidgets.QLabel(self.frame)

            # Adding style to the boxes

            add_style(self.Box_1)
            self.Box_1.setGeometry(QtCore.QRect(0, 0, 171, 161))
            add_style(self.Box_2)
            self.Box_2.setGeometry(QtCore.QRect(170, 0, 171, 161))
            add_style(self.Box_3)
            self.Box_3.setGeometry(QtCore.QRect(340, 0, 171, 161))
            add_style(self.Box_4)
            self.Box_4.setGeometry(QtCore.QRect(340, 160, 171, 161))
            add_style(self.Box_5)
            self.Box_5.setGeometry(QtCore.QRect(170, 160, 171, 161))
            add_style(self.Box_6)
            self.Box_6.setGeometry(QtCore.QRect(0, 160, 171, 161))
            add_style(self.Box_7)
            self.Box_7.setGeometry(QtCore.QRect(340, 320, 171, 161))
            add_style(self.Box_8)
            self.Box_8.setGeometry(QtCore.QRect(170, 320, 171, 161))
            add_style(self.Box_9)
            self.Box_9.setGeometry(QtCore.QRect(0, 320, 171, 161))


            self.label = QtWidgets.QLabel(self.centralwidget)
            self.label.setGeometry(QtCore.QRect(250, 10, 341, 41))
            font = QtGui.QFont()
            font.setFamily("Orator Std")
            font.setPointSize(26)
            self.label.setFont(font)
            self.label.setObjectName("label")
            self.MainWindow.setCentralWidget(self.centralwidget)
            self.menubar = QtWidgets.QMenuBar(self.MainWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
            self.menubar.setObjectName("menubar")
            self.MainWindow.setMenuBar(self.menubar)
            self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
            self.statusbar.setObjectName("statusbar")
            self.MainWindow.setStatusBar(self.statusbar)

            self.retranslateGameUi(self.MainWindow)
            QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
            self.boxes = [self.Box_1, self.Box_2, self.Box_3, self.Box_6, self.Box_5, self.Box_4, self.Box_9, self.Box_8, self.Box_7]
            if self.firstChoose:
                self.boxes[self.game.main()].setText(" O")
            for box in self.boxes:
                box.mousePressEvent = partial(self.clicked, box)

    # Starting the game

    def clicked(self, box, event):
        if box.text() == " ":
            box.setText(" X")
            self.game.updateBoxMap(self.boxes.index(box), "X")
            result = self.game.main()
            if isinstance(result, int):
                if self.game.checkOver() == False:
                    self.boxes[result].setText(" O")
                else:
                    self.boxes[result].setText(" O")
                    self.gameOver(self.game.checkOver())
            elif isinstance(result, str):
                self.gameOver(result)
            else:
                self.boxes[int(result[0])].setText(" O")
                self.gameOver(self.game.checkOver())
        else:
            self.alert("Alert!!", "Please click on a empty box")
    def alert(self, head, desc):
        m = QMessageBox()
        m.setIcon(QMessageBox.Warning)
        m.setStandardButtons(QMessageBox.Ok)
        m.setWindowTitle(head)
        m.setText(desc)
        y = m.exec_()

    def gameOver(self, string):
        m = QMessageBox()
        m.setIcon(QMessageBox.Information)
        m.setStandardButtons(QMessageBox.Ok)
        m.setWindowTitle("Game Over")
        m.setText(string)
        m.buttonClicked.connect(self.restartGame)
        y = m.exec_()

    def restartGame(self):
        for box in self.boxes:
            box.deleteLater()
        self.label.deleteLater()
        self.frame.deleteLater()
        QtCore.QCoreApplication.quit()
        status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Roll Dice", "Roll Dice"))
        self.Dice.setText(_translate("MainWindow", "ROLL DICE"))
        self.label.setText(_translate("MainWindow", "Roll the dice to choose who\'s gonna take the first play"))

    def retranslateGameUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Tic Tac Toe", "Tic Tac Toe"))
        self.Box_1.setText(_translate("MainWindow", " "))
        self.Box_2.setText(_translate("MainWindow", " "))
        self.Box_3.setText(_translate("MainWindow", " "))
        self.Box_4.setText(_translate("MainWindow", " "))
        self.Box_5.setText(_translate("MainWindow", " "))
        self.Box_6.setText(_translate("MainWindow", " "))
        self.Box_7.setText(_translate("MainWindow", " "))
        self.Box_8.setText(_translate("MainWindow", " "))
        self.Box_9.setText(_translate("MainWindow", " "))
        self.label.setText(_translate("MainWindow", "AI = X, User = X"))