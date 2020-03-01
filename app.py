import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
import json
import requests

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    print(type(req))
    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    #if req.get("result").get("action") != "shipping.cost":
    #    return {}
    result = req["queryResult"]
    parameters = result["parameters"]
    zone = parameters["banknames"]
    response1 = requests.get("https://api.bankofscotland.co.uk/open-banking/v2.2/atms")
    atm = json.loads(response1.text)
    cost = {'Federal bank':'6.85%', 'Ceva':'6.75%'}
    #zone ='Federal Bank'
    speech = "The interest rate of " + zone + " is " + str(cost[zone])
    q=atm["data"][0]["Brand"][0]["ATM"][0]["Location"]["PostalAddress"]["GeoLocation"]["GeographicCoordinates"]["Latitude"]

    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        #"contextOut": [],
        "source": "BankRates",
        "fulfillmentText":speech
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" %(port))

    app.run(debug=True, port=port, host='0.0.0.0')