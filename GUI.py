import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from const import *
from functools import partial

class GUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__(); # invoke init of super class(QtWidgets.QWidget), GUI() is child class of QtWidgets.QWidget

        self.CurTroop = '';
        self.AllTroops = [];
        self.LoadTroopsButton = QtWidgets.QPushButton(self);
        self.LoadTroopsButton.setText("Load Troops");
        self.LoadTroopsButton.move(50,20);
        self.LoadTroopsButton.clicked.connect(self.LoadTroops);

        self.TaskTimeMenu = QtWidgets.QDateTimeEdit(self);
        self.TaskTimeMenu.setCalendarPopup(True); ## calendar pop up for date setting
        self.TaskTimeMenu.setDisplayFormat("yyyy-MM-dd hh:mm:ss ap");
        self.TaskTime = QtCore.QDateTime.currentDateTime();
        self.TaskTimeMenu.setDateTime(self.TaskTime);
        self.TaskTime = self.TaskTime.toPyDateTime();
        self.TaskTimeMenu.dateTimeChanged.connect(self.TaskTimeChanged);

        self.hbox = QtWidgets.QHBoxLayout(self);
        self.TroopsBox = QtWidgets.QButtonGroup(self);

        self.ModeButton = QtWidgets.QComboBox(self);
        self.mode = c_mode_city; ## Default Mode Value
        self.ModeButton.addItem("攻城", QtCore.QVariant(c_mode_city));
        self.ModeButton.addItem("佔地", QtCore.QVariant(c_mode_tile));
        self.ModeButton.addItem("行軍", QtCore.QVariant(c_mode_move));
        self.ModeButton.currentIndexChanged.connect(self.ModeChanged);

        self.RepeatButton = QtWidgets.QComboBox(self);
        self.repeat = -1; ## Default Mode Value
        self.RepeatButton.addItem("不限次", QtCore.QVariant(-1));
        self.RepeatButton.addItem("1次", QtCore.QVariant(1));
        self.RepeatButton.addItem("2次", QtCore.QVariant(2));
        self.RepeatButton.addItem("3次", QtCore.QVariant(3));
        self.RepeatButton.currentIndexChanged.connect(self.RepeatChanged);

        self.DelayBox = QtWidgets.QLineEdit(self);
        self.delay = 0;
        self.DelayBox.setPlaceholderText('0 seconds');
        self.DelayBox.setValidator(QtGui.QIntValidator());
        self.DelayBox.editingFinished.connect(self.DelayChanged);

        self.TargetBox = QtWidgets.QLineEdit(self);
        self.target = [0,0];
        self.TargetBox.setPlaceholderText('ex: 123,456');
        self.TargetBox.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{1,},[0-9]{1,}")));
        self.TargetBox.editingFinished.connect(self.TargetChanged);
        
        self.setGeometry(400,400,300,200); ##GUI window location and size
        self.setWindowTitle('TKAutoClick');
        self.show();

    def LoadTroops(self):
        self.CurTroop = '';
        self.AllTroops = [];

        print('current button group', self.TroopsBox.buttons());
        # Find all troop from game and create button for each
        self.FindTroopsImg();
        for btn in self.TroopsBox.buttons():
            self.TroopsBox.removeButton(btn); ## Clear all existing buttons before recreate new ones
            btn.deleteLater();
            
        for troop in self.AllTroops: ##
            btn = QtWidgets.QPushButton(checkable = True);
            btn.setStyleSheet("checked{background-color: blue;}"); # set push button color when selected
            troop_img = QtGui.QPixmap(troop);
            print('Image size ', troop_img.width(), troop_img.height())
            btn.setFixedSize(troop_img.width(), troop_img.height());
            btn.setStyleSheet("background-image : url(" + troop + ");");
            btn.clicked.connect(partial(self.TroopSelected, troop)); #partial() create a new with argument replace by a constant(troop in this case)
            self.hbox.addWidget(btn);
            self.TroopsBox.addButton(btn);
        print('Loading Troops');

    def TroopSelected(self, troop):
        self.CurTroop = troop;
        print('Troop selected : ', troop);

    def TaskTimeChanged(self):
        self.TaskTime = self.TaskTimeMenu.dateTime().toPyDateTime();
        print('Task Time has changed to :', self.TaskTime);

    def ModeChanged(self):
        self.mode = self.ModeButton.currentData();
        print('Mode Changed to : ', self.mode);

    def RepeatChanged(self):
        self.repeat = self.RepeatButton.currentData();
        print('Repeat Changed to : ', self.repeat);

    def DelayChanged(self):
        self.delay = int(self.DelayBox.text());
        print('Delay Changed to : ', self.delay, ' seconds');

    def TargetChanged(self):
        self.target = self.TargetBox.text().split(',');
        print('Target Changed to : ', self.target);

    def FindTroopsImg(self):
        # this function find and capture img of troops for pyautogui to locate
        for troop_img_path in c_troops:
            #capture 5 available troops at specific location
            #if the capture image is invalid(no troop)
            if False:
                print('Invalid troop');
            else:
                self.AllTroops.append(troop_img_path);
                print('Found a troop');
            
        print('Found and saved all Images');

def GUI_Init():
    app = QtWidgets.QApplication(sys.argv);# contain the GUI application object
    gui = GUI();
    sys.exit(app.exec_());
    return gui;
	
if __name__ == '__main__':  #only run when as main
   gui = GUI_Init();
