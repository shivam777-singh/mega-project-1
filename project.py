import os
import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import openai
import music_libra

# Initialize the recognizer and text-to-speech engine
reco = sr.Recognizer()
itt = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    itt.say(text)
    itt.runAndWait()

# Function to process AI responses " it not work because we need plain to use ai in our code"
def aiprocess(given_data):
    openai.api_key = "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"  # Keep your actual API key here
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant."},
            {"role": "user", "content": given_data}
        ]
    )
    return completion.choices[0].message['content']

# Function to process the given command
def process(given_data):
    if given_data.lower() == "open google":
        webbrowser.open("https://google.com")
    elif given_data.lower() == "open youtube":
        webbrowser.open("https://youtube.com")
    elif given_data.lower() == "open facebook":
        webbrowser.open("https://facebook.com")
    elif given_data.lower().startswith("play"):
        song = given_data.split(" ", 1)[1]  # Split "play" and the song name, get the song name
        link = music_libra.music.get(song, None)  # Get the link from the dictionary
        if link:
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find the song {song}.")
    elif given_data.lower() == "give news":
        NEWS_API_URL = "https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=defe0876b2654e00a89587c393cc5b70"
        response = requests.get(NEWS_API_URL)
        news_data = response.json()
        articles = news_data.get('articles')
        headlines = [article['title'] for article in articles]
        for headline in headlines:
            speak(headline)
    else:
        output = aiprocess(given_data)
        speak(output)

# Main function to listen and process commands
if __name__ == "__main__":
    speak("Code started successfully.")
    while True:
        try:
            # Listen for the start word
            with sr.Microphone() as source:
                print("Say 'Jarvis' to start listening for commands.")
                audio = reco.listen(source, timeout=2, phrase_time_limit=2)
                command_for_start = reco.recognize_google(audio)  # Convert to text
            
            # If the start word is detected, proceed to listen for the actual command
            if command_for_start.lower() == "jarvis":
                speak("Yes, how can I help you?")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = reco.listen(source)
                    command_for_work = reco.recognize_google(audio)  # Convert to text
                
                # Process the given command
                process(command_for_work)
        
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you please repeat?")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            speak("An unexpected error occurred. Please try again.")
