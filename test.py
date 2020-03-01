import json
import requests

#print("test")
response = requests.get("https://still-escarpment-09649.herokuapp.com/bot/sharp/")
#atm = json.loads(response.text)

print(response)

#print(todos)