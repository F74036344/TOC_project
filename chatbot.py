import sys

import telegram
from flask import Flask, request
from transitions import Machine

# For webpage parsing
from bs4 import BeautifulSoup
import urllib.request
# import request

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
class LuckKeywords:
	def __init__(self):
		self.luckKeywords = [];

sign_keywords = SignKeywords()

# keywords = Keywords(
# 		['牡羊','白羊','Aries','aries','Ram','ram'],
# 		['金牛','Bull','bull','Taurus','taurus'],
# 		['雙子','Twins','twins','Twin','twin','Gemini','gemini'],
# 		['巨蟹','Crab','crab','Cancer','cancer'],
# 		['獅子','Lion','lion','Leo','leo'],
# 		['處女','Virgin','virgin','Virgo','virgo'],
# 		['天秤','天平','Balance','balance','Libra','libra'],
# 		['天蠍','Scorpion','scorpion','Scorpio','scorpio'],
# 		['射手','人馬','Archer','archer','Sagittarius','sagittarius'],
# 		['魔羯','山羊','Goat','goat','Capriocorn','capricorn'],
# 		['水瓶','寶瓶','Water','water','Aquarius','aquarius'],
# 		['雙魚','Fishes','fishes','Fish','fish','Pisces','pisces']
# 	)

# keywords = {
# 	'Ram': '牡羊座介紹',
# 	'Bull': '金牛座介紹',
# 	'Twins': '雙子座介紹',
# 	'Crab': '巨蟹座介紹',
# 	'Lion': '獅子座介紹',
# 	'Virgin': '處女座介紹',
# 	'Balance': '天秤座介紹',
# 	'Scorpion': '天蠍座介紹',
# 	'Archer': '射手座介紹',
# 	'Goat': '摩羯座介紹',
# 	'Aquarius': '水瓶座介紹',
# 	'Fish': '雙魚座介紹'
# }

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

def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)


@app.route('/hook', methods=['POST'])
def webhook_handler():
	if request.method == "POST":
		update = telegram.Update.de_json(request.get_json(force=True), bot)
		request_text = update.message.text
		update.message.reply_text(generate_reply_text(request_text))

	return 'ok'

def generate_reply_text(request_text):
	reply_text = request_text;
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
	# print(soup)
	if whichSign is not None:
		reply_text = reply_text + '(' + whichSign + ' keywords Detected XD)'
		page = urllib.request.urlopen(generate_url_to_parse(whichSign, 'daily', None))
		# Create parsing object 'soup'
		soup = BeautifulSoup(page, 'html.parser')
		luck_intro = soup.find('div', attrs={'class':'TODAY_CONTENT'}).text
		reply_text = luck_intro 


	return reply_text


def generate_url_to_parse(sign, time, luck_or_intro):
	# 網址形式: http://astro.click108.com.tw/daily.php?iAcDay=2017-06-02&iAstro=10
	time_option = time
	astro_option = str(astro_code[sign]);
	url = 'http://astro.click108.com.tw/' + time_option + '.php?' + 'iAstro=' + astro_option
	# + 'iAcDay=' + 
	return url

if __name__ == "__main__":
	_set_webhook()
	app.run()
