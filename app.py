# RESOURCE: http://www.apnorton.com/blog/2017/02/28/How-I-wrote-a-Groupme-Chatbot-in-24-hours/


# IMPORTS
import os
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request

app = Flask(__name__)
bot_id = "d38b2db8ef13f4f6e57b1c2d7c"

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

	elif text == '@Drumbot':
		reply('...I am listening')

	elif 'sniped' in textNoPunc.lower() != -1:
		reply('Gottem')

	elif 'shh' in textNoPunc.lower() != -1:
		reply('BITCH YOU GUESSED IT!')
		reply('HOO!')
		reply('...you was right')

	elif 'its 1024' in textNoPunc.lower() != -1:
		reply('GET LIT!!!')

	elif 'you guessed it' in textNoPunc.lower() != -1:
		reply('HOO!')
		reply('...you was right')

	elif 'aw yeah' in textNoPunc.lower() != -1:
		reply('BIG BOOTY!')

	elif 'litty titty' in textNoPunc.lower() != -1:
		reply('...tiiiiitttyyy liiiiitttyyyyyy...')

	elif 'theo' in textNoPunc.lower() != -1:
		reply('Theo\'s here! I\'m sober!')

	elif 'bitch' in textNoPunc.lower() != -1:
		reply('YOU GUESSED IT!')
		reply('HOO!')
		reply('...you was right')

	elif 'many' in textNoPunc.lower() != -1 and 'brick' in textNoPunc.lower() != -1:
		reply('Twelve Bricks')
		reply('(Sheesh! Damn!)')

	elif 'found twelve bricks' in textNoPunc.lower() != -1 or 'found 12 bricks' in textNoPunc.lower() != -1:
		reply('sheesh! damn!')

	elif 'trust me' in textNoPunc.lower() != -1:
		reply('...truss me daddy!')

	for i in range(len(words)):
		if words[i].lower() == 'big' and i == len(words) - 1:
			reply("...BOOTY!")

	if 'fuck' in textNoPunc.lower() != -1:
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
