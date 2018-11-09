# RESOURCE: http://www.apnorton.com/blog/2017/02/28/How-I-wrote-a-Groupme-Chatbot-in-24-hours/


# IMPORTS
import os
import json
import string
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request

app = Flask(__name__)
bot_id = "11562ca58f79256ffd68de861f"

# Called whenever the app's callback URL receives a POST request
# That'll happen every time a message is sent in the group
@app.route('/', methods=['POST'])
def webhook():
	# 'message' is an object that represents a single GroupMe message.
	message = request.get_json()

	translator = str.maketrans('', '', string.punctuation)
	text = message['text']
	textNoPunc = text.translate(translator)

	words = textNoPunc.split()

	if sender_is_bot(message):
		return "ok", 200


	if text == 'testing drumbot':
		reply('1,2,3')

	if text == 'spicy bus ten hut':
		reply('FUCK YOU!')

	elif text == '@Drumbot':
		reply('...I am listening')

	elif 'sniped' in textNoPunc.lower() != -1:
		reply('Gottem')

	elif 'shh' in textNoPunc.lower() != -1:
		reply('BITCH YOU GUESSED IT!')
		reply('HOO!')
		reply('...you was right')

	elif '1024' in textNoPunc.lower() != -1:
		reply('GET LIT!!!')

	elif 'you guessed it' in textNoPunc.lower() != -1:
		reply('HOO!')
		reply('...you was right')

	elif 'remember me to teefy crane' in textNoPunc.lower() != -1:
		reply('THAT BITCH!')

	elif 'tell them just how i' in textNoPunc.lower() != -1:
		reply('HUH!')

	elif 'lapping up the high high' in textNoPunc.lower() != -1:
		reply('BALLS BALLS BALLS BALLS')

	elif 'well all have' in textNoPunc.lower() != -1 or 'well all get' in textNoPunc.lower() != -1:
		reply('DRINKS!')

	elif 'at theodore' in textNoPunc.lower() != -1:
		reply('ZINK\'S!')

	elif 'penn' in textNoPunc.lower() != -1:
		reply('SUCKS!')

	elif 'harvard' in textNoPunc.lower() != -1:
		reply('*Hahvahd')

	elif 'aw yeah' in textNoPunc.lower() != -1:
		reply('BIG BOOTY!')

	elif 'litty titty' in textNoPunc.lower() != -1:
		reply('...tiiiiitttyyy liiiiitttyyyyyy...')

	elif 'its theo' in textNoPunc.lower() != -1 or 'theos here' in textNoPunc.lower() != -1:
		reply('Theo\'s here! I\'m sober!')

	elif 'many' in textNoPunc.lower() != -1 and 'brick' in textNoPunc.lower() != -1:
		reply('Twelve Bricks')
		reply('(Sheesh! Damn!)')

	elif 'found twelve bricks' in textNoPunc.lower() != -1 or 'found 12 bricks' in textNoPunc.lower() != -1:
		reply('sheesh! damn!')

	elif 'trust me' in textNoPunc.lower() != -1:
		reply('...truss me daddy!')
	
	elif 'we are percussion' in textNoPunc.lower() != -1:
		reply('FUCK YOU!')

	for i in range(len(words)):
		if i == len(words) - 1:
			if words[i].lower() == 'big':
				reply("...BOOTY!")

			if words[i].lower() == 'bees':
				reply("...are dying at an alarming rate. :(")

			if words[i].lower() == 'bitch':
				reply('YOU GUESSED IT!')
				reply('HOO!')
				reply('...you was right')

		if i == len(words) - 4:
			if words[i].lower() == 'dut' and words[i+1].lower() == 'dut' and words[i+2].lower() == 'dut' and words[i+3].lower() == 'dut':
				reply("BOI!")

		if i == len(words) - 2:
			if words[i].lower() == 'poop' and words[i+1].lower() == 'is':
				reply("BROWN!")

			if words[i].lower() == 'go' and words[i+1].lower() == 'red':
				reply("dammit!")

			if words[i].lower() == 'click' and words[i+1].lower() == 'click':
				reply("Click.")

	if 'fucking' in textNoPunc.lower() != -1:
		reply('*Fkin')
	elif 'fucked' in textNoPunc.lower() != -1:
		reply('*Fked')
	elif 'fucker' in textNoPunc.lower() != -1:
		reply('*Fker')
	elif 'fuck' in textNoPunc.lower() != -1:
		reply('*Fk')
	return "ok", 200

################################################################################

# Send a message in the groupchat
def reply(msg):
	url = 'https://api.groupme.com/v3/bots/post'
	data = {
		'bot_id'		: bot_id,
		'text'			: msg
	}
	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()

# Send a message with an image attached in the groupchat
def reply_with_image(msg, imgURL):
	url = 'https://api.groupme.com/v3/bots/post'
	urlOnGroupMeService = upload_image_to_groupme(imgURL)
	data = {
		'bot_id'		: bot_id,
		'text'			: msg,
		'picture_url'		: urlOnGroupMeService
	}
	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()
	
# Uploads image to GroupMe's services and returns the new URL
def upload_image_to_groupme(imgURL):
	imgRequest = requests.get(imgURL, stream=True)
	filename = 'temp.png'
	postImage = None
	if imgRequest.status_code == 200:
		# Save Image
		with open(filename, 'wb') as image:
			for chunk in imgRequest:
				image.write(chunk)
		# Send Image
		headers = {'content-type': 'application/json'}
		url = 'https://image.groupme.com/pictures'
		files = {'file': open(filename, 'rb')}
		payload = {'access_token': 'eo7JS8SGD49rKodcvUHPyFRnSWH1IVeZyOqUMrxU'}
		r = requests.post(url, files=files, params=payload)
		imageurl = r.json()['payload']['url']
		os.remove(filename)
		return imageurl

# Checks whether the message sender is a bot
def sender_is_bot(message):
	return message['sender_type'] == "bot"
