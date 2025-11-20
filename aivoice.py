
"""
🔥 Continuous Voice Assistant with WhatsApp Messaging
Features:
- Continuously listens after waking
- Speaks results for all tasks (time, date, year)
- Plays YouTube videos by name
- Controls YouTube (pause, resume, volume up/down)
- Opens WhatsApp Desktop/Web
- Sends WhatsApp messages safely via voice
- Searches Wikipedia and reads summary
- Tells jokes
- Always asks: "What is the next task?"
- Exits on "stop/exit/bye"
"""

import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import webbrowser
import pyjokes
import keyboard
import datetime
import os
import sys
import time

# -------------------- Setup TTS engine --------------------
engine = pyttsx3.init()
engine.setProperty('rate', 165)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # female voice

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# -------------------- Speech recognition --------------------
recognizer = sr.Recognizer()

def listen(timeout=5, phrase_time_limit=8):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            query = recognizer.recognize_google(audio)
            print(f"You: {query}")
            return query.lower()
        except Exception:
            return ""

# -------------------- Core feature functions --------------------
def tell_time():
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M %p")
    speak(f"The time is {time_str}.")

def tell_date():
    today = datetime.date.today()
    date_str = today.strftime("%A, %B %d, %Y")
    speak(f"Today is {date_str}.")

def open_youtube():
    speak("Opening YouTube.")
    webbrowser.open("https://www.youtube.com")

def play_song_on_youtube(song):
    speak(f"Playing {song} on YouTube.")
    pywhatkit.playonyt(song)

def search_wikipedia(topic):
    speak(f"Searching Wikipedia for {topic}")
    try:
        result = wikipedia.summary(topic, sentences=2)
        speak("According to Wikipedia:")
        speak(result)
        webbrowser.open(f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}")
    except Exception:
        speak("Sorry, I couldn't find that on Wikipedia.")

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

def control_youtube(action):
    if action == "pause" or action == "stop":
        keyboard.send("space")
        speak("Video paused.")
    elif action in ("play", "resume"):
        keyboard.send("space")
        speak("Video resumed.")
    elif "volume up" in action:
        for _ in range(3):
            keyboard.send("volume up")
        speak("Volume increased.")
    elif "volume down" in action:
        for _ in range(3):
            keyboard.send("volume down")
        speak("Volume decreased.")

def open_whatsapp():
    speak("Opening WhatsApp.")
    desktop_path = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\WhatsApp\\WhatsApp.exe"
    if os.path.exists(desktop_path):
        try:
            os.startfile(desktop_path)
            speak("WhatsApp Desktop opened.")
        except Exception:
            speak("Unable to open WhatsApp Desktop. Opening WhatsApp Web.")
            webbrowser.open("https://web.whatsapp.com")
    else:
        speak("WhatsApp Desktop not found. Opening WhatsApp Web.")
        webbrowser.open("https://web.whatsapp.com")

def send_whatsapp_message():
    """Send WhatsApp message via voice input safely"""
    try:
        speak("Who do you want to send the message to?")
        name = listen()
        if not name:
            speak("No contact detected.")
            return

        # Define your contacts here
        contacts = {
            "naina": "+91XXXXXXXXXX",    # Replace with real numbers
            "pranshu": "+91XXXXXXXXXX",
            "mum": "+91XXXXXXXXXX",
            "dad": "+91XXXXXXXXXX"
        }

        if name.lower() not in contacts:
            speak("Sorry, I couldn't find that contact.")
            return

        speak(f"What message should I send to {name}?")
        message = listen()
        if not message:
            speak("No message detected.")
            return

        speak(f"Sending message to {name}.")
        pywhatkit.sendwhatmsg_instantly(contacts[name.lower()], message, wait_time=10)
        speak("Message sent successfully.")

    except Exception as e:
        speak("Sorry, I could not send the message.")
        print(f"Error: {e}")

# -------------------- Main command processor --------------------
def process_command(command):
    command = command.lower()

    if "stop" in command or "exit" in command or "bye" in command:
        speak("Goodbye! Have a nice day.")
        sys.exit()

    elif "time" in command:
        tell_time()

    elif "date" in command:
        tell_date()

    elif "year" in command:
        speak(f"The current year is {datetime.datetime.now().year}.")

    elif "play" in command and "youtube" in command:
        song = command.replace("play", "").replace("on youtube", "").strip()
        play_song_on_youtube(song)

    elif command.startswith("play "):
        song = command.replace("play", "").strip()
        play_song_on_youtube(song)

    elif "open youtube" in command:
        open_youtube()

    elif "open whatsapp" in command:
        open_whatsapp()

    elif "send message" in command or "whatsapp message" in command:
        send_whatsapp_message()

    elif "pause" in command or "stop video" in command:
        control_youtube("pause")

    elif "resume" in command or "play video" in command:
        control_youtube("play")

    elif "volume up" in command:
        control_youtube("volume up")

    elif "volume down" in command:
        control_youtube("volume down")

    elif "wikipedia" in command or "who is" in command or "what is" in command:
        topic = command.replace("wikipedia", "").replace("who is", "").replace("what is", "").strip()
        search_wikipedia(topic)

    elif "joke" in command:
        tell_joke()

    else:
        speak("I'm not sure about that. Let me search it for you.")
        pywhatkit.search(command)

    speak("What is the next task?")

# -------------------- Start assistant continuously --------------------
def wish_user():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        greet = "Good morning"
    elif 12 <= hour < 17:
        greet = "Good afternoon"
    else:
        greet = "Good evening"
    speak(f"{greet}! I am your voice assistant. I am listening continuously. How can I help you today?")

def main():
    wish_user()
    while True:
        command = listen(timeout=10, phrase_time_limit=8)
        if command:
            process_command(command)
        else:
            speak("Sorry, I didn’t catch that. Please say it again.")
        time.sleep(1)

if __name__ == "__main__":
    main()
