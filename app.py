import speech_recognition as sr
import os
import webbrowser
import openai
import requests
from config import apikey, weather_api_key
import datetime
import platform

openai.api_key = apikey

chat_history = ""


def say(text):
    if platform.system() == 'Windows':
        os.system(
            f'powershell -Command "Add-Type -AssemblyName System.speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{text}\');"')
    else:
        os.system(f'say "{text}"')


def chat(query):
    global chat_history
    chat_history += f"User: {query}\nEcho AI: "
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chat_history,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer = response["choices"][0]["text"].strip()
        say(answer)
        chat_history += f"{answer}\n"
        return answer
    except Exception as e:
        print(f"Error: {e}")
        say("Sorry, I encountered an error.")
        return ""


def get_weather(location):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&units=metric"
        response = requests.get(url)
        weather_data = response.json()
        if weather_data["cod"] == 200:
            main = weather_data["weather"][0]["main"]
            description = weather_data["weather"][0]["description"]
            temp = weather_data["main"]["temp"]
            say(f"The weather in {location} is {main} with {description}. The temperature is {temp} degrees Celsius.")
        else:
            say("Sorry, I couldn't fetch the weather data.")
    except Exception as e:
        print(f"Error: {e}")
        say("Sorry, I couldn't fetch the weather data.")


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            say("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            say("Sorry, I am having trouble connecting to the service.")
            return ""
        except Exception as e:
            say("Some error occurred.")
            return ""


if __name__ == '__main__':
    print('Hey, this is Echo AI. How can I assist you today?')
    say("Hey, this is Echo AI. How can I assist you today?")

    query = take_command()

    if "what is the weather in" in query.lower():
        location = query.lower().split("in")[-1].strip()
        get_weather(location)

    elif "open" in query.lower():
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"]]
        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]}...")
                webbrowser.open(site[1])

    elif "play music" in query.lower():
        music_path = "C:\\Users\\YourUsername\\Downloads\\yourmusicfile.mp3"
        os.system(f'start {music_path}')

    elif "what is the time" in query.lower() or "current time" in query.lower():
        now = datetime.datetime.now().strftime("%H:%M")
        say(f"The current time is {now}")

    elif "quit" in query.lower():
        say("Goodbye!")
        exit()

    elif "reset chat" in query.lower():
        chat_history = ""

    else:
        chat(query)
