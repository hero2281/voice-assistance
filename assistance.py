import speech_recognition as sr
import datetime
import subprocess
import pywhatkit
import pyttsx3
import webbrowser

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
recognizer = sr.Recognizer()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def open_chrome():
    try:
        programName = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        subprocess.Popen([programName])
        speak("Chrome opened")
    except OSError:
        speak("Sorry, Chrome is not installed on this system.")

def get_current_time():
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    speak(f"The current time is {current_time}")

def play_youtube(query):
    speak("Opening YouTube...")
    pywhatkit.playonyt(query)

    # Pause listening temporarily while the YouTube video is playing
    recognizer.pause_threshold = 10  # Adjust the pause threshold as needed (in seconds)
    with sr.Microphone() as source:
        print("Pausing listening while YouTube video is playing...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        recognizer.pause_threshold = 0.5

        # Wait for the YouTube video to finish playing
        while pywhatkit.isPlaying():
            pass

    # Resume listening after the YouTube video has finished
    recognizer.pause_threshold = 0.5
    print("Resuming listening...")

def open_youtube():
    webbrowser.open('https://www.youtube.com')
    speak("Opening YouTube")

def handle_command(command):
    if 'chrome' in command:
        open_chrome()
    elif 'time' in command:
        get_current_time()
    elif 'play' in command:
        query = command.replace('play', '')
        play_youtube(query.strip())
    elif 'youtube' in command:
        open_youtube()
    else:
        speak("Sorry, I couldn't understand. Please try again.")

def listen_command():
    is_activated = False  # Flag to track activation
    while True:
        with sr.Microphone() as source:
            print("Clearing background noises... Please wait")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio, language='en_US')
                text = text.lower()
                print('Your message:', format(text))
                
                if 'Ramu' in text:
                    is_activated = True
                    speak("Hello... How can I help you?")
                elif is_activated:
                    return text.strip()
                else:
                    speak("I am not activated. Say my name...")
                    
            except sr.UnknownValueError:
                print("Sorry, I couldn't understand.")
                speak("Sorry, I couldn't understand. Please try again.")
            except sr.RequestError:
                print("Sorry, there was an issue with the speech recognition service.")
                speak("Sorry, there was an issue with the speech recognition service. Please try again.")
            except sr.WaitTimeoutError:
                print("Timeout: No speech detected.")
                speak("Timeout: No speech detected. Please try again.")


def main():
    while True:
        command = listen_command()
        if command is not None:
            handle_command(command)
        else:
            speak("No command detected. Do you want to try again?")  # Asking the user to try again
            response = listen_command()  # Listening for the user's response
            if response is not None and 'yes' in response:
                continue  # Continue the loop if the user wants to try again
            else:
                break  # Exit the loop if the user doesn't want to try again

if __name__ == '__main__':
    main()
