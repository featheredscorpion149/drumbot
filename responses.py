#!/usr/bin/env python3

# RESOURCE: http://www.apnorton.com/blog/2017/02/28/How-I-wrote-a-Groupme-Chatbot-in-24-hours/


# IMPORTS
import os
import json
import string
import random
from enum import Enum

class Condition(Enum):
        EXACT=1
        CONTAINS=2
        END=3
        AND=4

class Response:
        def __init__(self, trigger, response, conditions=Condition.CONTAINS):
                self.triggers = trigger
                self.response = response
                self.conditions = conditions
        def check(self, text, textNoPunc, words):
                if self.conditions == Condition.AND:
                        for t in self.triggers:
                                if textNoPunc.lower().find(t) == -1:
                                        return False
                        return True

                else:
                        for t in self.triggers:
                                if self.conditions == Condition.EXACT:
                                        if text == t:
                                                return True
                                elif self.conditions == Condition.CONTAINS:
                                        if (t in textNoPunc.lower() != -1):
                                                return True
                                elif self.conditions == Condition.END:
                                        lower = textNoPunc.lower().strip()
                                        index = lower.find(t)
                                        if index != -1 and index == len(lower) - len(t):
                                                return True

                return False
        def reply(self):
                return self.response

class RandomResponse:
        def __init__(self, trigger, prepend, responseList, conditions=Condition.CONTAINS):
                self.triggers = trigger
                self.prepend = prepend
                self.responseList = responseList
                self.conditions = conditions
        def check(self, text, textNoPunc, words):
                if self.conditions == Condition.AND:
                        for t in self.triggers:
                                if textNoPunc.lower().find(t) == -1:
                                        return False
                        return True

                else:
                        for t in self.triggers:
                                if self.conditions == Condition.EXACT:
                                        if text == t:
                                                return True
                                elif self.conditions == Condition.CONTAINS:
                                        if (t in textNoPunc.lower() != -1):
                                                return True
                                elif self.conditions == Condition.END:
                                        lower = textNoPunc.lower().strip()
                                        index = lower.find(t)
                                        if index != -1 and index == len(lower) - len(t):
                                                return True

                return False
        def reply(self):
                r = random.randint(0, len(self.responseList) - 1)
                return [self.prepend + " " + self.responseList[r]], None

responses = [

        Response(["boondoggle bus ten hut"], ["FUCK YOU"], Condition.CONTAINS),
        Response(["@Drumbot"], ["...I am listening"], Condition.EXACT),
        Response(["sniped"], ["Gottem"], Condition.CONTAINS),

        Response(["shh"], ["BITCH YOU GUESSED IT!", "HOO!", "...you was right"], Condition.CONTAINS),
        Response(["you guessed it", "u guessed it"], ["HOO!", "...you was right"], Condition.END),
        Response(["bitch"], ["YOU GUESSED IT!", "HOO!", "...you was right"], Condition.END),

        Response(["remember me to teefy crane", "remember me to the ja"], ["THAT BITCH!"], Condition.CONTAINS),
        Response(["1024", "ten twenty four"], ["GET LIT!!!"], Condition.CONTAINS),
        Response(["tell them just how i"], ["HUH!"], Condition.CONTAINS),
        Response(["lapping up the high high"], ["BALLS BALLS BALLS BALLS"], Condition.CONTAINS),
        Response(["well all have", "well all get"], ["DRINKS!"], Condition.CONTAINS),
        Response(["at theodore"], ["ZINK\'S!"], Condition.CONTAINS),

        Response(["penn"], ["SUCKS!"], Condition.CONTAINS),
        Response(["harvard"], ["*Hahvahd"], Condition.CONTAINS),
        Response(["aw yeah"], ["BIG BOOTY!"], Condition.CONTAINS),
        Response(["litty titty"], ["...tiiiiitttyyy liiiiitttyyyyyy..."], Condition.CONTAINS),
        Response(["its theo", "theos here"], ["I\'m sober!"], Condition.CONTAINS),
        Response(["trust me"], ["...truss me daddy!"], Condition.CONTAINS),
        Response(["we are percussion"], ["FUCK YOU!"], Condition.CONTAINS),
        Response(["fuck em up", "fuck um up", "fuck them up"], ["GO C U!"], Condition.CONTAINS),
        Response(["dont be that guy"], ["BE THAT GUY!"], Condition.CONTAINS),
        Response(["cold", "freezing"], ["Ha! Y'all are weak!"], Condition.CONTAINS),

        Response(["big"], ["...BOOTY!"], Condition.END),
        Response(["bees"], ["... are dying at an alarming rate. :("], Condition.END),
        Response(["dut dut dut dut"], ["BOI!"], Condition.END),
        Response(["poop is"], ["BROWN!"], Condition.END),
        Response(["brown is"], ["POOP!"], Condition.END),
        Response(["if its brown"], ["flush it down"], Condition.END),
        Response(["go red"], ["dammit!"], Condition.END),
        Response(["click click"], ["CLICK."], Condition.END),

        Response(["alumni status"], ["Did you mean: Alex Wong?"]),
        Response(["barbeque sauce", "bbq sauce"], ["THAT\'S HAZING!", "@Martha_Pollack"]),
        Response(["masturbate", "jack off", "masturbation", "jacking off"], ["That's a Band-Sanctioned event!"]),
        ]

ezra_responses = [
        Response(["institution", "motto"], ["I would found an institution where any person can find instruction in any study!"], Condition.CONTAINS),
        Response(["cornell", "ezra"], ["...you rang?"], Condition.CONTAINS),
        Response(["ithaca"], ["Sounds like a great place for a university."], Condition.CONTAINS),
        Response(["far above", "cayuga"], ["Ah yes, a majestic view."], Condition.AND),
        Response(["cayuga"], ["Man I love being far above that lake."], Condition.CONTAINS),
        Response(["slope"], ["In my day we walked up the slope BOTH WAYS."], Condition.CONTAINS),
]

oja_hazing = [
        "Of course it is! Please turn yourself in immediately.",
        "Hmmm... probably not, but we'll still JA you for it.",
        "Anything fun is hazing.",
        "We coooould suspend you for that, but instead we'll yell at you for an hour because we're nice :)",
        "Nah, that's fine. As long as you don't get caught..."
]

oja_responses = [
        Response(["tpose"], ["Please do not haze the OJA."], Condition.AND),
        Response(["is", "band event"], ["The OJA says: only if you're doing something bad."], Condition.AND),
        Response(["help"], ["The OJA isn't actually here to help you, sorry."]),

        RandomResponse(["is", "hazing"], "The OJA says:", oja_hazing, Condition.AND),

        Response([""], ["The OJA doesn't understand the question, but is still offended."]),
]

meme_responses = [
        Response(["that wasnt very cash money of you","thats not very cash money of you"], ["https://i.redd.it/7sut3n8k3w021.png"], Condition.CONTAINS),
        Response(["wack"], ["https://i.groupme.com/480x361.gif.2a7813806bae4dea8860208409cc5a74.large"], Condition.CONTAINS),
        Response(["wha"], ["https://i.kym-cdn.com/entries/icons/facebook/000/027/475/Screen_Shot_2018-10-25_at_11.02.15_AM.jpg"], Condition.CONTAINS),
        Response(["sign", "road"], ["https://i.groupme.com/480x351.gif.31a7339cfb0a46768aa9bc76ebff4b0d.large"], Condition.AND),
        Response(["brrrap", "brrap", "brap"], ["https://i.groupme.com/600x446.jpeg.a71923d48c17430d9e68fad1f1d5bac1.large"], Condition.CONTAINS),
]

def get_response(message):
        text = message
        translator = str.maketrans('', '', string.punctuation)
        textNoPunc = text.translate(translator)
        words = textNoPunc.split()

        #for r in ezra_responses:
        #        if r.check(text, textNoPunc, words):
        #                return r.reply()

        for r in responses:
                if r.check(text, textNoPunc, words):
                        return r.reply()

        for r in meme_responses:
                if r.check(text, textNoPunc, words):
                        return r.reply()

        for r in oja_responses:
                if text.find("@OJA") != -1 and r.check(text, textNoPunc, words):
                        return r.reply()

        return [], None

if __name__ == "__main__":
        # 'message' is an object that represents a single GroupMe message.
        message = ''
        while True:
                message = input("Enter message: ")
                words = get_response(message)
                for t in words:
                        print(t)
