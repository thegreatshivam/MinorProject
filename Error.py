# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/Error.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_errorDialog(object):
    def setupUi(self, errorDialog):
        errorDialog.setObjectName("errorDialog")
        errorDialog.resize(400, 262)
        self.label = QtWidgets.QLabel(errorDialog)
        self.label.setGeometry(QtCore.QRect(10, 30, 361, 131))
        self.label.setObjectName("label")
        self.backButton = QtWidgets.QPushButton(errorDialog)
        self.backButton.setGeometry(QtCore.QRect(150, 200, 93, 28))
        self.backButton.setStyleSheet("background-color: rgb(85, 255, 127);\n"
"font: 75 11pt \"MS Shell Dlg 2\";")
        self.backButton.setObjectName("backButton")
        self.backButton.clicked.connect(errorDialog.close)

        self.retranslateUi(errorDialog)
        QtCore.QMetaObject.connectSlotsByName(errorDialog)

    def retranslateUi(self, errorDialog):
        _translate = QtCore.QCoreApplication.translate
        errorDialog.setWindowTitle(_translate("errorDialog", "Error"))
        self.label.setText(_translate("errorDialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600; color:#ff0000;\">Something went wrong.</span></p><p align=\"center\"><span style=\" font-size:18pt; font-weight:600; color:#ff0000;\">Error Occurred.</span></p></body></html>"))
        self.backButton.setText(_translate("errorDialog", "Home"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    errorDialog = QtWidgets.QDialog()
    ui = Ui_errorDialog()
    ui.setupUi(errorDialog)
    errorDialog.show()
    sys.exit(app.exec_())