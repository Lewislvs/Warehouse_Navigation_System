from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Warehouse Map")
        Form.resize(1600, 900)
        self.center()
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(1330, 100, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.textEdit_time = QtWidgets.QTextEdit(Form)
        self.textEdit_time.setGeometry(QtCore.QRect(1310, 60, 261, 41))
        self.textEdit_time.setObjectName("textEdit_time")

        self.label_time = QtWidgets.QLabel(Form)
        self.label_time.setGeometry(QtCore.QRect(1330, 20, 261, 41))
        self.label_time.setFont(font)
        self.label_time.setObjectName("label_time")



        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(1310, 140, 261, 41))
        self.textEdit.setObjectName("textEdit")
        

        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(1330, 180, 261, 41))
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.textEdit2 = QtWidgets.QTextEdit(Form)
        self.textEdit2.setGeometry(QtCore.QRect(1310, 220, 261, 41))
        self.textEdit2.setPlaceholderText("ex.(1,2) Please input:1 2")
        self.textEdit2.setObjectName("textEdit2")



        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(1330, 260, 261, 41))
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.textEdit3 = QtWidgets.QTextEdit(Form)
        self.textEdit3.setGeometry(QtCore.QRect(1310, 300, 261, 41))
        self.textEdit3.setPlaceholderText("ex.(1,2) Please input:1 2")
        self.textEdit3.setObjectName("textEdit3")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(1340, 360, 91, 31))
        self.pushButton.setObjectName("pushButton")

        self.pushButton1 = QtWidgets.QPushButton(Form)
        self.pushButton1.setGeometry(QtCore.QRect(1440, 360, 91, 31))
        self.pushButton1.setObjectName("pushButton1")
        
        self.pushButton2 = QtWidgets.QPushButton(Form)
        self.pushButton2.setGeometry(QtCore.QRect(1390, 410, 91, 31))
        self.pushButton2.setObjectName("pushButton2")

        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(1330, 460, 261, 41))
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        self.textEdit4 = QtWidgets.QTextEdit(Form)
        self.textEdit4.setGeometry(QtCore.QRect(1310, 500, 261, 41))
        self.textEdit4.setPlaceholderText("ex.Order#1 Please input:1. For next unfulfilled order, empty this edit.")
        self.textEdit4.setObjectName("textEdit4")


        self.pushButton3 = QtWidgets.QPushButton(Form)
        self.pushButton3.setGeometry(QtCore.QRect(1340, 560, 91, 31))
        self.pushButton3.setObjectName("pushButton3")

        self.pushButton4 = QtWidgets.QPushButton(Form)
        self.pushButton4.setGeometry(QtCore.QRect(1440, 560, 91, 31))
        self.pushButton4.setObjectName("pushButton4")

        self.pushButton5 = QtWidgets.QPushButton(Form)
        self.pushButton5.setGeometry(QtCore.QRect(1390, 600, 91, 31))
        self.pushButton5.setObjectName("pushButton5")


        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(1400, 635, 71, 21))
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(1310, 660, 261, 192))
        self.textBrowser.setObjectName("textBrowser")
        

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Warehouse Navigation"))
        self.label_time.setText(_translate("Form", "Enter Time Limit(s)"))
        self.label.setText(_translate("Form", "Enter Product ID"))
        self.label_2.setText(_translate("Form", "Result"))
        self.label_3.setText(_translate("Form", "Enter Start Location"))
        self.label_4.setText(_translate("Form", "Enter End Location"))
        self.label_5.setText(_translate("Form", "Enter Order Number"))
        self.pushButton.setText(_translate("Form", "Search"))
        self.pushButton1.setText(_translate("Form", "BFSearch"))
        self.pushButton2.setText(_translate("Form", "Location"))
        self.pushButton3.setText(_translate("Form", "Search"))
        self.pushButton4.setText(_translate("Form", "BFSearch"))
        self.pushButton5.setText(_translate("Form", "Location"))

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
