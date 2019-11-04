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
        # A response takes a list of triggers, a list of responses, and a condition
        # ANY trigger on the list will cause the response
        # EVERY response will be sent to the group, in order, as seperate messages
        # Examples of conditions are shown below:

        # CONTAINS matches any string that contains the substring (default)
        Response(["sniped"], ["Gottem"], Condition.CONTAINS),

        # EXACT matches the exact string
        Response(["@Drumbot"], ["...I am listening"], Condition.EXACT),

        # END matches any string that ends in the substring
        Response(["bees"], ["... are dying at an alarming rate. :("], Condition.END),

        # AND matches any string that contains every substring
        Response(["slope", "steep"], ["Ha! Get better leg muscles!"], Condition.AND),
        ]

# These post pictures using the URL
meme_responses = [
        Response(["wack"], ["https://i.groupme.com/480x361.gif.2a7813806bae4dea8860208409cc5a74.large"], Condition.CONTAINS),
]

def get_response(message):
        text = message
        translator = str.maketrans('', '', string.punctuation)
        textNoPunc = text.translate(translator)
        words = textNoPunc.split()

        for r in responses:
                if r.check(text, textNoPunc, words):
                        return r.reply()

        for r in meme_responses:
                if r.check(text, textNoPunc, words):
                        return r.reply()

        return []

if __name__ == "__main__":
        # 'message' is an object that represents a single GroupMe message.
        message = ''
        while True:
                message = input("Enter message: ")
                words = get_response(message)
                for t in words:
                        print(t)
