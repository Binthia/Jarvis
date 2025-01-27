import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from musicLibrary import music

# pip install speechrecognition pyaudio
# pip install setuptools
# pip install pyttsx3
# pip install pocketsphinx

recognizer=sr.Recognizer()
ttsx=pyttsx3.init()
newsapi="--------------------------"

def speak(text):
    ttsx.say(text)
    ttsx.runAndWait()

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

if __name__ ==  "__main__":
    speak("Hii mam I am Jarvis")

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