import speech_recognition as sr
import pyttsx3
import random
from greetings import *
import datetime

# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_command():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        command = command.lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand.")
    except sr.RequestError:
        print("Sorry, there was an issue with the speech recognition service.")

def handle_command(command):
    current_time = datetime.datetime.now().time()
    current_hour = current_time.hour

    if 'hello' in command:
        if current_hour < 12:
            speak(random.choice(morning_greetings))
        elif current_hour < 17:
            speak(random.choice(day_greetings))
        else:
            speak(random.choice(evening_greetings))

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The current time is {current_time}.")

    elif 'goodbye' in command:
        speak(random.choice(farewell_greetings))
        exit()

    else:
        speak("Sorry, I couldn't understand. Can you please repeat?")

def main():
    speak("Hello! How can I assist you?")
    while True:
        command = listen_command()
        if command:
            handle_command(command)

if __name__ == '__main__':
    main()
