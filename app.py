import urllib
import json
import os
import pgeocode
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


    if "geo-city" in parameters.keys():
        city = parameters["geo-city"]
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
        speech=maxName+" has the most ATMs in "+city +", with a total of "+str(max)
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
        
    if "age" in parameters.keys():
        n=parameters['age']
        #speech="you are "+str(int(n))+" years old"
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
        #atm = json.loads(response1.text)
        #cost = {'Federal bank':'6.85%', 'Ceva':'6.75%'}
        #zone ='Federal Bank'
        #speech = "The interest rate of " + zone + " is " + str(cost[zone])
        
        #
        #q=atm["data"][0]["Brand"][0]["ATM"][0]["Location"]["PostalAddress"]["GeoLocation"]["GeographicCoordinates"]["Latitude"]
    d3={
        "Bank Of Scotland":"PCA/scotland.json",
        "Barclays Bank":"PCA/barclays.json",
        "HSBC Group":"PCA/hsbc.json",
        "Lloyds Bank":"PCA/lloyds.json",
        "Santander UK PLC":"PCA/santander.json"
    }
    d4={}
    d5={
        "Bank Of Scotland":10,
        "Barclays Bank":8,
        "HSBC Group":7,
        "Lloyds Bank":5,
        "Santander UK PLC":4
    }
    for x in d3.keys():
        #data=requests.get(d[x])
        with open(d3[x], 'r') as myfile:
            data=myfile.read()
            d4[x]=json.loads(data)


    if "segment" in parameters.keys():
        spendingType = ''
        if "spender" in parameters.keys():
            spendingType = parameters['spender']
        s=parameters['segment']
        max=1000000
        name=""
        min=20
        for j in d3.keys():
            sum=0
            count=0
            l=d4[j]["data"][0]["Brand"][0]['PCA']

            for a in range(len(l)-1):
                print(l[a].keys())
                if 'Segment' in l[a]:
                    if(l[a]['Segment'][0]==s):
                        print(spendingType)
                        if spendingType == 'High':
                            if 'Overdraft' in l[a]['PCAMarketingState'][0].keys():
                                path = l[a]['PCAMarketingState'][0]['Overdraft']['OverdraftTierBandSet'][0]['OverdraftTierBand'][0]
                                if "TierValueMax" in path.keys():
                                    print(path['TierValueMax'])
                                    if float(path['TierValueMax']) < float(max):
                                        name=j + " has the lowest overdraft of that type so you don't overspend to much"
                                        max = path['TierValueMax']
                        if name == "":
                            print("here")
                            count+=1
                            if(d5[j]<=min):
                                name=j + "is the highest rated bank offering that option"
                                min=d5[j]
        
        speech= name
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
      

    if "zip-code" in parameters.keys():
        getcode = parameters["zip-code"]
        nomi = pgeocode.Nominatim('gb')
        post = nomi.query_postal_code(getcode)
        myCity = post['place_name']
        myCity=myCity.split(",")[0]
        print(myCity)
        myLat = post['latitude']
        myLong = post['longitude']
        distance = 10000000
        speech="default"
        max=0
        maxName=""
        flag=0
        count = 0
        for k in d1.keys():
            sum=0
            q=d2[k]["data"][0]["Brand"][0]["ATM"]
            for i in range(len(q)):
                if "TownName" in q[i]["Location"]["PostalAddress"].keys():
                    if "TownName" in q[i]["Location"]["PostalAddress"].keys():
                        p = q[i]["Location"]["PostalAddress"]["TownName"]
                        if myCity == p:
                            count += 1
                            getcode = q[i]["Location"]["PostalAddress"]["PostCode"]
                            post = nomi.query_postal_code(getcode)
                            thisDist = 0
                            thisLat = post['latitude']
                            thisLong = post['longitude']
                            thisDist = (thisLat-myLat)*(thisLat-myLat)+(thisLong-myLong)*(thisLong-myLong)
                            print(thisDist)
                            if thisDist < distance:
                                distance = thisDist
                                getaddress = q[i]["Location"]["PostalAddress"]
                                speech = getaddress['BuildingNumber'] + " "+ getaddress['StreetName'] + " " + getaddress['PostCode']
        speech = speech + '\n There are a total of ' + str(count) + " ATM's in your city"
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