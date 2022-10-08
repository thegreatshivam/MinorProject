import speech_recognition as sr
import pyaudio
import wave
import frontEnd

window = frontEnd.Main()


r = sr.Recognizer()

with sr.AudioFile('recording.wav') as source:
    audio_text = r.listen(source)

try:
    text = r.recognize_google(audio_text)
    print(text)
except Exception:
    print("Something happened")
