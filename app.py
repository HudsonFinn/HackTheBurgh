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
    city = parameters["geo-city"]
    """
    d={
        #"Bank of Ireland (UK) plc":"https://api.bankofscotland.co.uk/open-banking/v2.2/atms",
        "Bank Of Scotland":"https://api.bankofscotland.co.uk/open-banking/v2.2/atms",
        "Barclays Bank":"https://atlas.api.barclays/open-banking/v2.2/atms",
        "Halifax":"https://api.halifax.co.uk/open-banking/v2.2/atms",
        "Danske Bank":"https://obp-data.danskebank.com/open-banking/v2.2/atms",
        "First Trust Bank":"https://openapi.firsttrustbank.co.uk/open-banking/v2.2/atms",
        "HSBC Group":"https://api.hsbc.com/open-banking/v2.2/atms",
        "Lloyds Bank":"https://api.lloydsbank.com/open-banking/v2.2/atms",
        "Nationwide Building Society":"https://openapi.nationwide.co.uk/open-banking/v2.2/atms",
        "NatWest":"https://openapi.natwest.com/open-banking/v2.2/atms",
        "Royal Bank of Scotland":"https://openapi.rbs.co.uk/open-banking/v2.2/atms",
        "Santander UK PLC":"https://openbanking.santander.co.uk/sanuk/external/open-banking/v2.2/atms",
        "Ulster Bank North":"https://openapi.ulsterbank.co.uk/open-banking/v2.2/atms"
    }
    
    """
    d1={
        "Bank Of Scotland":"atms/scotland.json",
        "Barclays Bank":"atms/barclays.json",
        "HSBC Group":"atms/hsbc.json",
        "Lloyds Bank":"atms/lloyds.json",
        "Santander UK PLC":"atms/santander.json"
    }


    d2={}
    for x in d1.keys():
        #data=requests.get(d[x])
        with open(d1[x], 'r') as myfile:
            data=myfile.read()
            d2[x]=json.loads(data)



    d3={
        "Bank Of Scotland":"PCA/scotland.json",
        "Barclays Bank":"PCA/barclays.json",
        "HSBC Group":"PCA/hsbc.json",
        "Lloyds Bank":"PCA/lloyds.json",
        "Santander UK PLC":"PCA/santander.json"
    }
    d4={}
    for x in d1.keys():
        #data=requests.get(d[x])
        with open(d3[x], 'r') as myfile:
            data=myfile.read()
            d4[x]=json.loads(data)

    

    max=0
    maxName=""
    flag=0
    for k in d1.keys():
        sum=0
        q=d2[k]["data"][0]["Brand"][0]["ATM"]
        for i in range(len(q)):
            if "TownName" in q[i]["Location"]["PostalAddress"].keys():
                p = q[i]["Location"]["PostalAddress"]["TownName"]
                if p == city:
                    sum+=1
                if(sum>=max):
                    max=sum
                    maxName=k


    

    #atm = json.loads(response1.text)
    #cost = {'Federal bank':'6.85%', 'Ceva':'6.75%'}
    #zone ='Federal Bank'
    #speech = "The interest rate of " + zone + " is " + str(cost[zone])
    
    speech=maxName+" has the most ATMs in "+city +", with a total of "+str(max)
    #q=atm["data"][0]["Brand"][0]["ATM"][0]["Location"]["PostalAddress"]["GeoLocation"]["GeographicCoordinates"]["Latitude"]

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