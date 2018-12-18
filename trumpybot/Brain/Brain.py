################################################################################
## Brain                                                                      ##
## TrumpyBot's "Brain." Houses the Text to Speech and Speech to Text engines  ##
## and calls the Twitter API based on prompts.                                ##
################################################################################

import os
import json
import speech_recognition as speech

import timekeeper


class Brain:
    def __init__(self):
        self.recent_command = ""
        self.output = ""
        self.active = True
        self.state = 'LISTEN'

        with open("profile/data.json") as file_data:
            profile = json.load(file_data)
            self.city = profile["city"]
            self.user = profile["user"]

        print("Brain module loaded")

    def listen(self):
        if not self.state == 'LISTEN':
            return

        recognizer = speech.Recognizer()

        with speech.Microphone() as source:
            audio = recognizer.listen(source)

        with open("transcripts/recent.wav", "wb") as recording:
            recording.write(audio.get_wav_data())

        try:
            command = recognizer.recognize_google(audio)
            self.recent_command = command.lower()
        except speech.UnknownValueError:
            self.recent_command = "Unknown Error"
        except speech.RequestError:
            self.recent_command = "Request Error"

        print(self.recent_command)

    def speak(self):
        if not self.output:
            return

        for output in self.output:
            os.system("espeak \"" + output + "\"")

        self.output = []

    def interpret(self):
        if self.recent_command == "":
            return

        self.state = 'COMMAND'
        keywords = set(self.recent_command.split(' '))

        names = ["bibo", "bubo", "fubo",
                 "bhutto", "bebo", "boohbah",
                 "leader", "trump", "trumpy"]
        names = set(names)

        if not names.intersection(keywords):
            self.state = 'LISTEN'
            return

        command = self.recent_command.split()
        command = [word for word in command if word not in names]
        self.recent_command = ' '.join(command)

        if "time" in keywords:
            self.output = timekeeper.time_report()
        elif "praise" in keywords:
            self.output = "Supreme Leader Trump watches over our great freedom land"
        elif "sleep" in keywords:
            self.active = False
            self.output = ["Goodnight"]
            self.speak()
            return

        self.speak()
        self.recent_command = ""
        self.state = 'LISTEN'
        return