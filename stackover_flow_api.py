import requests
import json

response = requests.get('https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow')

for questions in response.json()['items']:
    if questions['answer_count']== 0:
        print(questions['title'])
        print(questions['link'])
        print()
    else:
        print('skipped')
    print()