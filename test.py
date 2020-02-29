import json
import requests

#print("test")
response = requests.get("https://api.bankofscotland.co.uk/open-banking/v2.2/atms")
atm = json.loads(response.text)

print(atm["data"][0])

#print(todos)