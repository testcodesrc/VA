import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import os
import tkinter as tk
from tkinter import messagebox
import time
import threading


# Initialize the speech engine
engine = pyttsx3.init()

# Set rate and volume
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

# Function to talk
def talk(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to your voice command
def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for a command...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio)  # Using Google's speech recognition API
        print(f"Command received: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        talk("Sorry, I didn't understand that.")
        return None
    except sr.RequestError:
        print("Sorry, I'm having trouble reaching the server.")
        talk("Sorry, I'm having trouble reaching the server.")
        return None

# Function to process commands
def process_command(command):
    if 'hello' in command:
        talk("Hello, how can I assist you?")
    elif 'what is your name' in command:
        talk("I am your personal assistant.")
    elif 'open' in command:
        if 'website' in command:
            talk("Opening website.")
            webbrowser.open('https://www.google.com')
        else:
            talk("Opening default browser.")
            webbrowser.open('https://www.google.com')
    elif 'search' in command:
        topic = command.replace("search", "").strip()
        talk(f"Searching for {topic} on Wikipedia.")
        try:
            result = wikipedia.summary(topic, sentences=2)
            print(result)
            talk(result)
        except wikipedia.exceptions.DisambiguationError as e:
            talk("There are multiple results, please be more specific.")
        except wikipedia.exceptions.HTTPTimeoutError:
            talk("Sorry, the search took too long. Try again later.")
    elif 'play music' in command:
        talk("Playing music now.")
        os.system("start wmplayer")  # Windows default media player
    elif 'exit' in command or 'bye' in command:
        talk("Goodbye!")
        exit(0)
    else:
        talk("Sorry, I did not understand that command.")

# Function to start listening in the background thread
def start_listening():
    while True:
        command = listen()
        
        if command:
            process_command(command)
        
        time.sleep(1)  # Prevent constant listening without break

# Function to handle the button press for listening
def start_assistant():
    talk("Hello, I am your voice assistant. How can I help you today?")
    listening_thread = threading.Thread(target=start_listening, daemon=True)
    listening_thread.start()

# GUI
class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")
        self.root.geometry("400x300")
        self.root.config(bg="lightblue")
        
        # Title Label
        self.title_label = tk.Label(self.root, text="Voice Assistant", font=("Helvetica", 18, "bold"), bg="lightblue")
        self.title_label.pack(pady=20)

        # Start Button
        self.start_button = tk.Button(self.root, text="Start Listening", font=("Helvetica", 14), command=start_assistant)
        self.start_button.pack(pady=20)

        # Instruction Label
        self.instruction_label = tk.Label(self.root, text="Click the button to start listening to commands.", font=("Helvetica", 12), bg="lightblue")
        self.instruction_label.pack(pady=20)

        # Quit Button
        self.quit_button = tk.Button(self.root, text="Quit", font=("Helvetica", 12), command=self.root.quit)
        self.quit_button.pack(pady=10)
        
        # Optional: Add Logo
        # self.logo = tk.PhotoImage(file="assets/logo.png")
        # self.logo_label = tk.Label(self.root, image=self.logo, bg="lightblue")
        # self.logo_label.pack()

# Main function to run the GUI
def run_gui():
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()

if __name__ == "__main__":
    # Run the GUI in the main thread
    run_gui()