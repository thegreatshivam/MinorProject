import speech_recognition as sr
import wave
import pyaudio
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QFileDialog, QDialog
from Error import Ui_errorDialog
from Output import Ui_outputDialog


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.setFixedSize(800, 600)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.recordButton = QtWidgets.QPushButton(self.centralwidget)
        self.recordButton.setGeometry(QtCore.QRect(80, 40, 231, 171))
        self.recordButton.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";")
        self.recordButton.setObjectName("recordButton")
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(80, 300, 231, 171))
        self.stopButton.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";")
        self.stopButton.setObjectName("stopButton")
        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(430, 300, 231, 171))
        self.exitButton.setStyleSheet("color:rgb(255, 0, 0);\n"
                                      "font: 75 20pt \"Yu Gothic UI\";")
        self.exitButton.setObjectName("exitButton")
        self.selectButton = QtWidgets.QPushButton(self.centralwidget)
        self.selectButton.setGeometry(QtCore.QRect(430, 40, 231, 171))
        self.selectButton.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.selectButton.setObjectName("selectButton")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

        self.mainWindow = mainWindow

        self.resume = False
        self.frames = []

        self.recordButton.clicked.connect(self.record)
        self.selectButton.clicked.connect(self.select)
        self.stopButton.clicked.connect(self.stop)
        self.stopButton.setEnabled(False)
        self.exitButton.clicked.connect(self.exit)

    def record(self):
        self.stopButton.setEnabled(True)
        self.recordButton.setEnabled(False)
        self.selectButton.setEnabled(False)
        self.exitButton.setEnabled(False)
        self.frames = []
        global audio
        audio = pyaudio.PyAudio()
        global stream
        stream = audio.open(format=pyaudio.paInt16, channels=2, rate=48000, input=True, frames_per_buffer=1024)
        self.resume = True
        print("Recording")
        self.recording()

    def recording(self):
        if self.resume:
            data = stream.read(1024)
            self.frames.append(data)
            QtCore.QTimer.singleShot(1, self.recording)

    def stop(self):
        print("Stopped")
        self.resume = False
        stream.stop_stream()
        stream.close()
        audio.terminate()

        sound_file = wave.open("recording.wav", "wb")
        sound_file.setnchannels(2)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(self.frames))
        sound_file.close()
        self.convert()
        self.stopButton.setEnabled(False)
        self.recordButton.setEnabled(True)
        self.selectButton.setEnabled(True)
        self.exitButton.setEnabled(True)

    def convert(self):
        r = sr.Recognizer()

        with sr.AudioFile('recording.wav') as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio_text = r.listen(source)

        try:
            # Offline recognition
            # text = r.recognize_sphinx(audio_text, language="en-IN")
            # Online recognition
            text = r.recognize_google(audio_text)
            print(text)
            self.win = QtWidgets.QDialog()
            self.ui = Ui_outputDialog()
            self.ui.setupUi(self.win)
            self.ui.textBox.setPlainText(text)
            self.win.exec_()

        except Exception:
            print("Something happened")
            self.win = QtWidgets.QDialog()
            self.ui = Ui_errorDialog()
            self.ui.setupUi(self.win)
            self.win.exec_()

    def select(self):
        print("selecting")
        options = QFileDialog.Options()
        fileName, test = QFileDialog.getOpenFileName(self.mainWindow, "Choose File", "", "Audio Files (*.mp3 *.wav)",
                                                     options=options)
        if test:
            f = open(fileName, 'r')
            f_name = f.name
            if f.name[-3::1] == "mp3":
                print(f.name)
                f_name = f.name + ".wav"
                import subprocess
                #Set the path of ffmpeg.exe below
                subprocess.call(['ffmpeg', '-y', '-i', f.name,
                                 f_name])

            r = sr.Recognizer()

            with sr.AudioFile(f_name) as source:
                audio_text = r.record(source)
            try:
                # Offline recognition
                # text = r.recognize_sphinx(audio_text, language="en-IN")
                # Online recognition
                text = r.recognize_google(audio_text)
                print(text)
                self.win = QtWidgets.QDialog()
                self.ui = Ui_outputDialog()
                self.ui.setupUi(self.win)
                self.ui.textBox.setPlainText(text)
                self.win.exec_()

            except Exception as e:
                print(e + "Something happened")
                self.win = QtWidgets.QDialog()
                self.ui = Ui_errorDialog()
                self.ui.setupUi(self.win)
                self.win.exec_()

    def exit(self):
        print("Quiting")
        mainWindow.close()

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Voice to Text GUI"))
        self.recordButton.setText(_translate("mainWindow", "Record"))
        self.stopButton.setText(_translate("mainWindow", "Stop"))
        self.exitButton.setText(_translate("mainWindow", "Exit"))
        self.selectButton.setText(_translate("mainWindow", "Select an Audio File"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
