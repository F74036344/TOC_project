import sys

import telegram
from flask import Flask, request
from transitions import Machine

# For webpage parsing
from bs4 import BeautifulSoup
import urllib.request
# import request
import random
import time, datetime

#為了畫FSM的圖(不知道為什麼pygraphviz無法裝到我的電腦上所以先註解掉)
# from transitions.extensions import GraphMachine as Machine 

API_TOKEN = '360313119:AAGJOkRmXF2wxcqwEkujI47qrRotks7XS2I'
# You can get the API token from the BotFather on the Telegram
WEBHOOK_URL = 'https://30234fb8.ngrok.io/hook'
# e.g. 'https://Your URL/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)

# 希望能夠做出一個星座的聊天機器人，功能有:
# (1) 能夠回答出各個星座的"人格特質"
# (2) 能夠回答出各個星座的"運勢"(今日、明日、本周、本年等)
# (需要去parse星座運勢網站)

# 建立Finite State Machine
class Matter(object):
    pass

lump = Matter()
# lump = Model() # 筆誤?
# The states
states=['welcome', 'waiting', 'sign_intro', 'luck_intro', 'unknown_msg']

# And some transitions between states. We're lazy, so we'll leave out
# the inverse phase transitions (freezing, condensation, etc.).
transitions = [
    { 'trigger': 'welcome_to_waiting', 'source': 'welcome', 'dest': 'waiting' },
    { 'trigger': 'sign', 'source': 'waiting', 'dest': 'sign_intro' },
    { 'trigger': 'luck', 'source': 'waiting', 'dest': 'luck_intro' },
    { 'trigger': 'unknown', 'source': 'waiting', 'dest': 'unknown_msg' },
    { 'trigger': 'lambda_luck_back', 'source': 'luck_intro', 'dest': 'waiting' },
    { 'trigger': 'lambda_sign_back', 'source': 'sign_intro', 'dest': 'waiting' },
    { 'trigger': 'lambda_unknown_back', 'source': 'unknown_msg', 'dest': 'waiting' }
]

# Initialize
machine = Machine(model=lump, states=states, transitions=transitions, initial='welcome')

# 輸出整個FSM的圖
# lump.get_graph().draw('my_FSM_diagram.png', prog='dot')

# 建立星座dictionary

# Keywords of signs
class SignKeywords:
    def __init__(self):
        self.Ram = ['牡羊','白羊','Aries','aries','Ram','ram']
        self.Bull = ['金牛','Bull','bull','Taurus','taurus']
        self.Twins = ['雙子','Twins','twins','Twin','twin','Gemini','gemini']
        self.Crab = ['巨蟹','Crab','crab','Cancer','cancer']
        self.Lion = ['獅子','Lion','lion','Leo','leo']
        self.Virgin = ['處女','Virgin','virgin','Virgo','virgo']
        self.Balance = ['天秤','天平','Balance','balance','Libra','libra']
        self.Scorpion = ['天蠍','Scorpion','scorpion','Scorpio','scorpio']
        self.Archer = ['射手','人馬','Archer','archer','Sagittarius','sagittarius']
        self.Goat = ['魔羯','山羊','Goat','goat','Capriocorn','capricorn']
        self.Aquarius = ['水瓶','寶瓶','Water','water','Aquarius','aquarius']
        self.Fish = ['雙魚','Fishes','fishes','Fish','fish','Pisces','pisces']
        self.Intro = ['介紹','簡介','特質','特點','Feature','feature','Intro','intro']
        self.Luck = ['luck','']
class TimeKeywords:	# 此class keywords需搭配signKeyword
	def __init__(self):
		self.today = ['今','today','Today']
		self.tomorrow = ['明','tomorrow','Tomorrow']
		self.week = ['週','周','week','Week']
		self.month = ['月','month','Month']
class LuckKeywords:
	def __init__(self):
		self.luckKeywords = ['運勢','luck','Luck']
class IntroKeywords:
	def __init__(self):
		self.introKeywords = ['個性','介紹','特質','intro','Intro','feature','Feature']

class UnknownWord:
	def __init__(self):
		self.unknownWord = ['不好意思聽不懂你的問題喔，麻煩請再說清楚一些><，可以用下面的方式問我問題喔~\n例如: 我想知道金牛座明天的運勢~']
	def genUnknownWord(self):
		return self.unknownWord[0]

sign_keywords = SignKeywords()
time_keywords = TimeKeywords()
luck_keywords = LuckKeywords()
intro_keywords = IntroKeywords()
unknown_word = UnknownWord()

# Introductions of signs
# build up the astro code dictionary ( for webpage parsing)
astro_code = {
	'Ram': 0,
	'Bull': 1,
	'Twins': 2,
	'Crab': 3,
	'Lion': 4,
	'Virgin': 5,
	'Balance': 6,
	'Scorpion': 7,
	'Archer': 8,
	'Goat': 9,
	'Aquarius': 10,
	'Fish': 11
}


def generate_reply_text(request_text):
	reply_text = request_text;
	# 抓關鍵字
	# 抓星座關鍵字
	whichSign = None;
	if any(ext in request_text for ext in sign_keywords.Ram): whichSign = 'Ram'
	elif any(ext in request_text for ext in sign_keywords.Bull): whichSign = 'Bull'
	elif any(ext in request_text for ext in sign_keywords.Twins): whichSign = 'Twins'
	elif any(ext in request_text for ext in sign_keywords.Crab): whichSign = 'Crab'
	elif any(ext in request_text for ext in sign_keywords.Lion): whichSign = 'Lion'
	elif any(ext in request_text for ext in sign_keywords.Virgin): whichSign = 'Virgin'
	elif any(ext in request_text for ext in sign_keywords.Balance): whichSign = 'Balance'
	elif any(ext in request_text for ext in sign_keywords.Scorpion): whichSign = 'Scorpion'
	elif any(ext in request_text for ext in sign_keywords.Archer): whichSign = 'Archer'
	elif any(ext in request_text for ext in sign_keywords.Goat): whichSign = 'Goat'
	elif any(ext in request_text for ext in sign_keywords.Aquarius): whichSign = 'Aquarius'
	elif any(ext in request_text for ext in sign_keywords.Fish): whichSign = 'Fish'
	# 抓時間關鍵字
	whichTime = None;
	if any(ext in request_text for ext in time_keywords.today): whichTime = 'today'
	elif any(ext in request_text for ext in time_keywords.tomorrow): whichTime = 'tomorrow'
	elif any(ext in request_text for ext in time_keywords.week): whichTime = 'week'
	elif any(ext in request_text for ext in time_keywords.month): whichTime = 'month'
	# 抓運勢關鍵字
	isLuck = False;
	if any(ext in request_text for ext in luck_keywords.luckKeywords): isLuck = True
	# 抓介紹關鍵字
	isIntro = False;
	if any(ext in request_text for ext in intro_keywords.introKeywords): isIntro = True


	if whichSign is not None:
		if whichTime is not None:
			page = urllib.request.urlopen(generate_url_to_parse(whichSign, whichTime, None))
		else:
			page = urllib.request.urlopen(generate_url_to_parse(whichSign, 'today', None))
		# Create parsing object 'soup'
		soup = BeautifulSoup(page, 'html.parser')
		luck_intro = soup.find('div', attrs={'class':'TODAY_CONTENT'}).text
		reply_text = luck_intro
		return reply_text 

	else:
		return unknown_word.genUnknownWord()



def generate_url_to_parse(sign, timeOp, luck_or_intro):
	# 網址形式: http://astro.click108.com.tw/daily.php?iAcDay=2017-06-02&iAstro=10&iType=4
	# astro_option
	astro_option = str(astro_code[sign]);
	# time_option, time_date, type_option
	# init
	type_option = ''
	if timeOp == 'today':
		time_option = 'daily'
		time_date = getDate('today')
	elif timeOp == 'tomorrow':
		time_option = 'daily'
		time_date = getDate('tomorrow')
		type_option = '&iType=4'
	elif timeOp == 'week':
		time_option = 'weekly'
		time_date = getDate('today')
		type_option = '&iType=1'
	elif timeOp == 'month':
		time_option = 'monthly'
		time_date = getDate('today')
		type_option = '&iType=2'
	url = ('http://astro.click108.com.tw/' + time_option + '.php?' 
		+ 'iAstro=' + astro_option
		+ '&iAcDay=' + time_date
		+ type_option
		)
	return url

## yyyy-mm-dd format
def getDate(whichDay):
	#Create a datetime object with today's value
	today = datetime.datetime.today() 
	#add one day to today's date
	tomorrow = today + datetime.timedelta(1)

	#print today's date in YYYY-MM-DD format
	if whichDay == 'today':	
		return datetime.datetime.strftime(today,'%Y-%m-%d')
	elif whichDay == 'tomorrow':
		#print tomorrow's date in YYYY-MM-DD format
		return datetime.datetime.strftime(tomorrow,'%Y-%m-%d')


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    	# telegram.Update.message.reply_text('\(^o^)/')

@app.route('/hook', methods=['POST'])
def webhook_handler():
	if request.method == "POST":
		update = telegram.Update.de_json(request.get_json(force=True), bot)
		request_text = update.message.text
		update.message.reply_text(generate_reply_text(request_text))
	return 'ok'

if __name__ == "__main__":
	_set_webhook()
	app.run()
