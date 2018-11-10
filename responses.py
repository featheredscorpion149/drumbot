#!/usr/bin/env python3

# RESOURCE: http://www.apnorton.com/blog/2017/02/28/How-I-wrote-a-Groupme-Chatbot-in-24-hours/


# IMPORTS
import os
import json
import string
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

responses = [
        Response(["barbeque bus ten hut"], ["FUCK YOU"], Condition.CONTAINS),
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
        Response(["its theo", "theos here"], ["Theo\'s here!", "I\'m sober!"], Condition.CONTAINS),
        Response(["trust me"], ["...truss me daddy!"], Condition.CONTAINS),
        Response(["we are percussion"], ["FUCK YOU!"], Condition.CONTAINS),
        Response(["dont be that guy"], ["BE THAT GUY!"], Condition.CONTAINS),
        Response(["if its brown"], ["FUCK YOU!"], Condition.CONTAINS),


        Response(["big"], ["...BOOTY!"], Condition.END),
        Response(["bees"], ["... are dying at an alarming rate. :("], Condition.END),
        Response(["dut dut dut dut"], ["BOI!"], Condition.END),
        Response(["poop is"], ["BROWN!"], Condition.END),
        Response(["brown is"], ["POOP!"], Condition.END),
        Response(["go red"], ["dammit!"], Condition.END),
        Response(["click click"], ["CLICK."], Condition.END),

        Response(["alumni status"], ["Did you mean: Alex Wong?"]),
        Response(["barbeque sauce", "bbq sauce"], ["THAT\'S HAZING!", "@Martha_Pollack"]),
        Response(["masturbate", "jack off", "masturbation", "jacking off"], ["That's a Band-Sanctioned event!"]),
        ]

oja_responses = [
        Response(["t-pose"], ["Please do not haze the OJA."], Condition.AND),
        Response(["is", "hazing"], ["The OJA says: of course it is! Please turn yourself in immediately."], Condition.AND),
        Response(["is", "a band event"], ["The OJA says: only if you're doing something bad."], Condition.AND),
        Response(["help"], ["The OJA isn't actually here to help you, sorry."]),

        Response([""], ["The OJA doesn't understand the question, but is still offended."]),
]

def get_response(message):
        text = message
        translator = str.maketrans('', '', string.punctuation)
        textNoPunc = text.translate(translator)
        words = textNoPunc.split()

        for r in responses:
                if r.check(text, textNoPunc, words):
                        return r.reply()

        for r in oja_responses:
                if text.find("@OJA") != -1 and r.check(text, textNoPunc, words):
                        return r.reply()

        return []

if __name__ == "__main__":
        # 'message' is an object that represents a single GroupMe message.
        message = ''
        while True:
                message = input("Enter message: ")
                for t in get_response(message):
                        print(t)
