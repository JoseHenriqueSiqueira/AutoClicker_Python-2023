from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from pynput import keyboard
import sys, pyautogui, re

class MainWindow(QMainWindow):
    signal=pyqtSignal(str)
    def __init__(self):
        super().__init__()
        loadUi(r"Ui's/Interface.ui",self)
        self.setWindowTitle("AutoClicker")
        self.setWindowIcon(QIcon(r"Images/MainIMG.png"))
        self.setFixedSize(317,125)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()
        self.signal.connect(self.signalResponse)
        self.run=False
        self.key=False
        self.inputs = [self.inputS, self.inputD, self.inputC, self.inputM] #Gets the variables responsible for the Second, Tenth of a Second, Hundredth of a Second and Milesinth of a Second. That way, we don't need to repeat each separate variable to assign a value or attribute.
        self.clicks = { #This dict is responsible for assigning items to the ComboBox "clickbox" and for avoiding the creation of many if-elses to know which click the user wants to repeat
            "LeftClick": pyautogui.leftClick,
            "RightClick": pyautogui.rightClick,
            "MiddleClick": pyautogui.middleClick,
            "DoubleLeft": lambda: pyautogui.doubleClick(button='left'),
            "DoubleRight": lambda: pyautogui.doubleClick(button='right'),
            "DoubleMiddle": lambda: pyautogui.doubleClick(button='middle')
        }
        self.clickbox.addItems(self.clicks.keys()) #Adding the keys to the comboBox
        self.clickbox.currentIndexChanged.connect(self.options)# Connects the ComboBox item change to the options() function
        for input in self.inputs: #Creating a small loop to assign the maximum size and Validator of all inputs(QLineEdit())
            input.setMaxLength(1)
            input.setValidator(QRegExpValidator(QRegExp("^[0-9]*$")))
        self.btnkey.clicked.connect(lambda: (self.btnkey.setText("..."), setattr(self, "key", True))) #Assigns the text "..." to the "btnkey" button and "True" to the "self.key" variable
        self.qtimer = QTimer(self) #Creating a QTimer
        self.qtimer.timeout.connect(pyautogui.click) #Connecting Qtimer to the Pyautogui module click() method

    def on_key_press(self, key):
        key = re.sub("(Key\.|'|<|>)","", str(key)).upper()
        numbers={
            "96":'0',
            "97":"1",
            "98":"2",
            "99":"3",
            "100":"4",
            "101":"5",
            "102":"6",
            "103":"7",
            "104":"8",
            "105":"9",
            "110":",",
        }
        key = numbers.get(key) if numbers.get(key) else key
        if key and self.key:
            self.btnkey.setText(key)
            self.key=False
            return
        if key == self.btnkey.text():
            self.signal.emit("Start")

    def signalResponse(self,response):
        if response=="Start":
            self.start_auto_click()

    def options(self):
        index=self.clickbox.currentText() #Getting the key (current Text) of the ComboBox
        self.qtimer.disconnect() #Disconnecting the Qtimer the previous click option set
        self.qtimer.timeout.connect(self.clicks[index]) #Connecting the selected click option by the user

    def start_auto_click(self):
        [input.setEnabled(False) for input in self.inputs] #Disable all inputs
        self.run = not self.run #Inverting the current value of the variable 'self.run'
        self.timer=int(self.inputS.text()+self.inputD.text()+self.inputC.text()+self.inputM.text()) #Concatenates the Second, Tenth, Hundredth and Thousandth numbers and transforms them into Integer values
        if self.run:
            self.qtimer.start(self.timer) #Starting QTimer with the value of self.timer
            self.btnkey.setEnabled(False) #Disable 'btnkey' to avoid errors
            self.clickbox.setEnabled(False) #Disable 'clickbox' to avoid errors
            return
        else:
            self.qtimer.stop() #Stopping QTimer
            self.btnkey.setEnabled(True) #Enable 'btnkey'
            self.clickbox.setEnabled(True) #Enable 'clickbox'
        [input.setEnabled(True) for input in self.inputs] #Enable all Inputs

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Main = MainWindow()
    Main.show()
    sys.exit(app.exec_())