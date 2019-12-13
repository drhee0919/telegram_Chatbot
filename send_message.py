import requests
from decouple import config

#API 기본요청사항 
url = 'https://api.telegram.org'
#token = '1035709474:AAHLKwX5i9uywZOJx8mGabDVCHSSP4quGJI'
token = config('TELEGRAM_BOT_TOKEN')
#chat_id = requests.get(f'{url}/bot{token}/getUpdates').json()["result"][0]["message"]["from"]["id"]
chat_id = config('CHAT_ID')
text = input('메시지를 입력하세요: ')

#상기 구성요소 변수들로 url 구조를 잡아주자
send_message = requests.get(f'{url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}') 

print(send_message.text)
