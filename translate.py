import requests
from decouple import config 

#https://cloud.google.com/translate/docs/quickstart참조 
url ='https://translation.googleapis.com/language/translate/v2'   
key =config('GOOGLE_TOKEN')  #구글키

data = {
    'q' : '엄마 판다는 새끼가 있네',
    'source' : 'ko',
    'target' : 'en'
}
result = requests.post(f'{url}?key={key}',data).json()
print(result)


