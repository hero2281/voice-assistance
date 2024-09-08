import speech_recognition as sr
import pyttsx3
from chatter import query
from functions import *
import datetime
import time

# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[8].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_command():
    with sr.Microphone() as source:
        # print("Listening...")
        audio = recognizer.listen(source)
    try:
        # print("Recognizing...")
        command = recognizer.recognize_google(audio)
        command = command.lower()
        print("You:", command)
        return command
    except sr.UnknownValueError:
        print("Bot: Sorry, I couldn't understand.")
    except sr.RequestError:
        print("Bot: Sorry, there was an issue with the speech recognition service.")

def handle_command(command):
    if "play" in command:
        print("Bot: Opening YouTube...")
        speak("Opening YouTube...")
        play_youtube(command)

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M:%S")
        print(f"Bot: It is {current_time}.")
        speak(f"It is {current_time}.")

    elif "send whatsapp message" in command or "send a whatsapp message" in command or "send message" in command or "send a message" in command:
        send_whatsapp_message(command)

    else:
        reply = query(command)
        try:
            reply = reply['generated_text']
            print("Reply: ", reply)
            speak(reply)
        except:
            print("Bot: Sorry, I couldn't understand.")
            speak("Sorry, I couldn't understand. Could you repeat.")

def send_whatsapp_message(command):
    message = command.replace("send whatsapp message", "").strip()
    print("Bot: Please provide the recipient's phone number.")
    speak("Please provide the recipient's phone number.")
    # recipient = listen_command()
    recipient = input("> ")
    time.sleep(1)
    print("Bot: Type the message to send.")
    speak("Type the message to send.")
    message = input("> ")

    if recipient:
        try:
            speak("Please wait. Sending WhatsApp message...")
            pywhatkit.sendwhatmsg(recipient, message, time.localtime().tm_hour, time.localtime().tm_min + 1)
            print(f"Bot: Message '{message}' sent to {recipient} successfully.")
            speak("Message sent successfully.")
        except Exception as e:
            print("Bot: Sorry, I encountered an error while sending the WhatsApp message.")
            speak("Sorry, I encountered an error while sending the WhatsApp message.")
            print(str(e))
    else:
        print("Bot: Phone number not provided. Please try again.")
        speak("Phone number not provided. Please try again.")

def main():
    print("Bot: Hello! How can I assist you?")
    speak("Hello! How can I assist you?")
    while True:
        command = listen_command()
        if command:
            handle_command(command)

if __name__ == '__main__':
    main()
