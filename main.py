import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
import pywhatkit
import datetime
import wikipedia
import pyjokes
import openai

import requests
import json
import pyttsx3

listener = sr.Recognizer()
openai.api_key = 'YOUR_OPEN_AI_API_KEY'  # Replace with your OpenAI API key

# Replace 'YOUR_OPENWEATHERMAP_API_KEY' with your OpenWeatherMap API key
openweathermap_api_key = 'YOUR_OPENWEATHERMAP_API_KEY'


# Replace 'YOUR_NEWS_API_KEY' with your News API key
news_api_key = 'YOUR_NEWS_API_KEY'


def say(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    male_voice = None
    for voice in voices:
        if 'male' in voice.name.lower():
            male_voice = voice
            break
    if male_voice:
        engine.setProperty('voice', male_voice.id)
    engine.say(text)
    with open("conversation.txt", "a") as f:
        f.write("Assistant: " + text + "\n")
    engine.runAndWait()
    engine.stop()


def take_command():
    command = ''
    try:
        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source)
            audio = listener.listen(source)
            command = listener.recognize_google(audio)
            command = command.lower()
            if 'hey kalam' in command:
                command = command.replace('hey kalam', '')
                print(command)
    except:
        pass
    return command


def generate_response(prompt):
    response = openai.Completion.create(
        engine='davinci',
        prompt=prompt,
        temperature=0.6,
        max_tokens=10,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text.strip()


def get_weather(city):
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'units': 'metric',
        'appid': openweathermap_api_key
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if data['cod'] == '404':
            say('City not found. Please try again.')
        else:
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            weather_info = f"The weather in {city} is {weather_description}. " \
                           f"The temperature is {temperature} degrees Celsius. " \
                           f"The humidity is {humidity}% and the wind speed is {wind_speed} meters per second."
            say(weather_info)
    except:
        say('Sorry, I encountered an error while fetching weather information.')


def get_news():
    base_url = 'https://newsapi.org/v2/top-headlines?country=in&apiKey=80c8f3d6f8c947baa57b4d2db58ba64c'
    params = {
        'country': 'india',
        'apiKey': news_api_key
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        articles = data['articles']
        headlines = [article['title'] for article in articles]
        news_info = '. '.join(headlines)
        say(news_info)
    except:
        say('Sorry, I encountered an error while fetching news.')


def run_kalam():
    city = 'Ankleshwar'  # Define the city here
    with open("conversation.txt", "a") as f:
        f.write("Kalam: Welcome to Kalam, your virtual assistant!\n")

    while True:
        command = take_command()
        print(command)
        with open("conversation.txt", "a") as f:
            f.write("User: " + command + "\n")

        if 'using ai' in command:
            user_query = command.replace('using ai', '')
            response = generate_response(user_query)
            say(response)
        elif 'play' in command:
            song = command.replace('play', '')
            say('Sure! Playing ' + song)
            pywhatkit.playonyt(song)
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            say('Sure! The current time is ' + time)
        elif 'who is' in command:
            person = command.replace('who the heck is', '')
            say('Let me find information about ' + person)
            info = wikipedia.summary(person, 1)
            print(info)
            say(info)
        elif 'date' in command:
            say('Sorry, I have a headache')
        elif 'are you single' in command:
            say('No, I am in a committed relationship with Wi-Fi')
        elif 'joke' in command:
            say('Sure! Here is a joke for you')
            joke = pyjokes.get_joke()
            print(joke)
            say(joke)
        elif 'how are you' in command:
            say("I am an AI assistant. I don't have feelings, but thanks for asking!")
        elif 'your name' in command:
            say('I am Kalam, your virtual assistant')
        elif 'weather' in command:
            say('Sure! Fetching weather information...')
            get_weather(city)
        elif 'news' in command:
            say('Sure! Fetching news headlines...')
            get_news()
        elif 'best school in ankleshwar' in command:
            say('The best school in Ankleshwar is P. P. Savani School Garden City.')
        elif 'goodbye' in command or 'bye' in command:
            say('Goodbye! Have a great day!')
            with open("conversation.txt", "a") as f:
                f.write("Kalam: Goodbye! Have a great day!\n")
            break
        else:
            say('I didn\'t understand the command. Please say it again.')
            with open("conversation.txt", "a") as f:
                f.write("Kalam: I didn't understand the command. Please say it again.\n")


if __name__ == '__main__':
    run_kalam()
