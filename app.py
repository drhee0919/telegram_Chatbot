import requests, pprint, random 
from flask import Flask, render_template, request
from decouple import config 
app = Flask(__name__)   #https://flask.palletsprojects.com/en/1.1.x/quickstart/ 에서 코드 참조

#텔레그램 API
url = 'https://api.telegram.org'
token = config('TELEGRAM_BOT_TOKEN')
chat_id = config('CHAT_ID')
#text = input('메시지를 입력하세요: ')

#구글 API
google_url ='https://translation.googleapis.com/language/translate/v2'   
google_key =config('GOOGLE_TOKEN')

@app.route('/')
def hello_world():
    return '메시지 봇'

@app.route(f'/{token}', methods=['POST']) #post방식을 쓰고 싶어서 쓰는 건 아니고 telegram이 그리말함 
def telegram():
    #1. 텔레그램이 보내주는 데이터 구조 확인 
    pprint.pprint(request.get_json())
    #2. 사용자 아이디, 메시지 추출
    chat_id = request.get_json().get('message').get('chat').get('id')
    message = request.get_json().get('message').get('text')

    #사용자가 로또라고 입력하면 로또 번호 6개 돌려주기
    if message == '로또':
        result = str(sorted(random.sample(range(1,46), 6)))
    
    #사용자가 /번역 이라고 말하면 한-영 번역 제공 
    elif message[:4] == '/번역 ':
        data = {
            'q': message[4:],
            'source': 'ko',
            'target': 'en',
            'format': 'text'
        }
        #1. 구글 API 번역 요청 
        response = requests.post(f'{google_url}?key={google_key}', data).json()
        #2. 번역 결과 추출 → 답장 변수에 저장 
        # translate.py 출력결과 입력 
        result = response['data']['translations'][0]['translatedText']
    # 그 외의 경우엔 메아리
    else:
        result = message

    #3. 텔레그램 API에 요청해서 답장 보내주기 
    requests.get(f'{url}/bot{token}/sendMessage?chat_id={chat_id}&text={result}')
    return '', 200
# https://api.telegram.org/bot1035709474:AAHLKwX5i9uywZOJx8mGabDVCHSSP4quGJI/getWebhookInfo

@app.route('/write')
def write():
    return render_template('write.html')

@app.route('/send')
def send():
    #1. 사용자가 입력한 데이터 받아오기
    message = request.args.get('message') #request(flask library)

    #2. 텔레그램 API 메시지 전송 요청 보내기 
    requests.get(f'{url}/bot{token}/sendMessage?chat_id={chat_id}&text={message}')    #requests(python library)    

    return render_template('send.html')




#반드시 파일 최하단에 위치시킬것 
if __name__ == '__main__':
    app.run(debug=True)



##Telegram 봇 생성 및 요청 보내보기 
## 봇 만들기
#BotFather → newbot → name입력 → username입력 
#토큰값 임시 저장하기(→ 메모장!)

## ※ (https://api.telegram.org/bot<내토큰번호>/METHOD_NAME)
## 요청 보내보기 
#[API 요청 주소]
#getMe메서드를 사용해서 내 봇에 대한 정보를 받아온다. (주소창 JSON형태) 
#https://api.telegram.org/bot1035709474:AAHLKwX5i9uywZOJx8mGabDVCHSSP4quGJI/getMe

#[메시지 이력 확인]
#https://api.telegram.org/bot1035709474:AAHLKwX5i9uywZOJx8mGabDVCHSSP4quGJI/getUpdates

#[나의 CHAT ID] -getUpdates 메소드로 JSON 확인 
#1042049696

#[send Message 샘플] 
#https://api.telegram.org/bot1035709474:AAHLKwX5i9uywZOJx8mGabDVCHSSP4quGJI/sendMessage?#chat_id=1042049696&text="안녕하세요"



#[배포용 도메인 만들기]
#https://api.telegram.org/bot1035709474:AAHLKwX5i9uywZOJx8mGabDVCHSSP4quGJI/setWebhook?url=https://drhee0919.pythonanywhere.com/1035709474:AAHLKwX5i9uywZOJx8mGabDVCHSSP4quGJI