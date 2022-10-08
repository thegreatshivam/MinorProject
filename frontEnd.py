import tkinter as tk
import wave
import pyaudio
from globals import *


class Main:

    def __init__(self):
        self.resume = False

        self.window = tk.Tk()
        self.window.title("Welcome")
        self.window.geometry("1024x768")

        start_button = tk.Button(self.window, text="Start", command=self.start)
        stop_button = tk.Button(self.window, text="Stop", command=self.stop)
        exit_button = tk.Button(self.window, text="Exit", command=self.window.destroy)

        start_button.pack()
        stop_button.pack()
        exit_button.pack()

        self.window.mainloop()

    def start(self):
        global audio
        audio = pyaudio.PyAudio()
        global stream
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44000, input=True, frames_per_buffer=1024)
        self.resume = True
        print("Recording")
        self.recording()

    def recording(self):
        if self.resume:
            data = stream.read(1024)
            frames.append(data)
        self.window.after(1, self.recording)

    def stop(self):
        print("Stopped")
        self.resume = False
        stream.stop_stream()
        stream.close()
        audio.terminate()

        sound_file = wave.open("recording.wav", "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44000)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()
