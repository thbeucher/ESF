import requests

URL = "http://api.microsofttranslator.com/v3/json/paraphrase"

TOKEN = "e58394eda89b4e4d856f9bcb37597447"

text = 'Je voudrais commander une pizza'

payload = {'appId': TOKEN, 'language': 'en', 'sentence': text, 'maxTranslations': 5}

r = requests.get(URL, params=payload)
print(r.url)

print(r.text)
