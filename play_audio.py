# play_audio.py
from playsound import playsound

def play_reminder():
    try:
        playsound("static/alert.mp3")
    except:
        print("Audio play failed.")
