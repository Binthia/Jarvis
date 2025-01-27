import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import pygame
import os
from musicLibrary import music
from openai import OpenAI
from gtts import gTTS

# pip install speechrecognition pyaudio
# pip install setuptools
# pip install pyttsx3
# pip install pocketsphinx
# pip install gTTS

recognizer=sr.Recognizer()
ttsx=pyttsx3.init()
newsapi="-------------------"

def speak_old(text):
    ttsx.say(text)
    ttsx.runAndWait()

def speak(text):
    tts=gTTS("text")
    tts.save('temp.mp3')

    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    clock=pygame.time.Clock()
    while pygame.mixer.music.get_busy():
        clock.tick(10)
    pygame.mixer.music.stop()  
    pygame.mixer.quit() 
    os.remove("temp.mp3")

def aiProcess(command):
    client=OpenAI(api_key="------------------")

    completion=client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role":"system","content":"You are a virtual assistent named Jarvis skilled in general tasks like Alexa and Google cloud give short responses"},
        {"role":"user","content":command}
    ]
    )
    return completion.choices[0].message["content"]

def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link=music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code==200:
            data=r.json()
            articles=data.get("articles",[])
            for article in articles:
                speak(article["title"])
    else:
        output=aiProcess(c)
        speak(output)

if __name__ ==  "__main__":
    speak("Hii mam I am Jarvis...")

while True:
    r=sr.Recognizer()
    print("Recognizing...")

    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio=r.listen(source,timeout=3,phrase_time_limit=3)
        word=r.recognize_google(audio)
        print(word)

        if(word.lower()=="jarvis"):
            speak("Yaaaa..")

            with sr.Microphone() as source:
                print("Jarvis Active...")
                audio=r.listen(source,timeout=3,phrase_time_limit=3)
                command=r.recognize_google(audio)

                processcommand(command)   #call function

    except Exception as e:
        print("Error; {0}".format(e))