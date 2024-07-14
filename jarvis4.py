import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import random
import os
import openai

# Initialize the recognizer and the text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Initialize OpenAI
openai.api_key = 'Add your API key here'  # Replace with your OpenAI API key

# Function to make the assistant speak
def talk(text):
    print(f"Jarvis says: {text}")  # Debug print
    engine.say(text)
    engine.runAndWait()

# Function to listen and recognize the command
def take_command():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)
            print('Listening...')
            audio = listener.listen(source)
            print('Processing...')
            command = listener.recognize_google(audio)
            command = command.lower()
            print(f"Recognized command: {command}")
            return command
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        talk("Sorry, I did not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        talk("Sorry, I couldn't connect to the speech recognition service.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        talk("An error occurred.")
        return None

# Function to tell the current time
def tell_time():
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    talk(f'Current time is {current_time}')

# Function to open a website
def open_website(url, site_name=None):
    if site_name:
        talk(f'Opening {site_name}')
    webbrowser.open(url)

# Function to tell a joke
def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the math book look sad? Because it had too many problems.",
        "What do you call fake spaghetti? An impasta!"
    ]
    joke = random.choice(jokes)
    talk(joke)

# Function to set a reminder (simplified example)
def set_reminder(task):
    talk(f'Setting a reminder for {task}')
    # For a real application, you would store this reminder somewhere persistent

# Function to play a song on YouTube
def play_song_on_youtube(song):
    talk(f'Playing {song} on YouTube')
    # Implement your code to play the song on YouTube here

# Function to get information from OpenAI
def ask_openai(question):
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=question,
            max_tokens=100
        )
        answer = response.choices[0].text.strip()
        return answer  # Return the text response from OpenAI
    except Exception as e:
        print(f"An error occurred with OpenAI API: {e}")
        talk("Sorry, I couldn't get a response from OpenAI.")
        return None

# Function to handle the recognized command
def handle_command(command):
    if 'open youtube' in command:
        open_website('https://www.youtube.com', 'YouTube')
    elif 'time' in command:
        tell_time()
    elif 'open google' in command:
        open_website('https://www.google.com', 'Google')
    elif 'open facebook' in command:
        open_website('https://www.facebook.com', 'Facebook')
    elif 'tell me a joke' in command:
        tell_joke()
    elif 'remind me to' in command:
        task = command.replace('remind me to', '').strip()
        set_reminder(task)
    elif 'open' in command:
        site_name = command.replace('open', '').strip()
        url = f'https://{site_name}'
        open_website(url, site_name)
    elif 'play' in command and ('on youtube' in command or 'in youtube' in command):
        song = command.replace('play', '').replace('on youtube', '').replace('in youtube', '').strip()
        play_song_on_youtube(song)
    elif 'ask openai' in command:
        question = command.replace('ask openai', '').strip()
        answer = ask_openai(question)
        if answer:
            talk(answer)  # Speak the answer retrieved from OpenAI
    else:
        talk(f'You said: {command}')
        talk('I am not sure how to help with that. Please try another command.')

# Main function to run Jarvis
def run_jarvis():
    talk('I am your Jarvis. What can I do for you?')
    command = take_command()
    if command:
        if 'jarvis' in command:
            command = command.replace('jarvis', '').strip()
            handle_command(command)
        else:
            talk('No trigger word "Jarvis" found in the command. Please say "Jarvis" and then your command.')
    else:
        talk('I did not understand. Please say it again.')

if __name__ == "__main__":
    run_jarvis()
