import pyttsx3 #pip install pyttsx3

def Speak(Text):
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voices',voices[1].id)
    engine.setProperty('rate',170)
    print("")
    print(f"{Text}.")
    print("")
    engine.say(Text)
    engine.runAndWait()

# Speak('hello')
