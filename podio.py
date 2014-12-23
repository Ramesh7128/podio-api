import requests
import json
import time
from podiodetails import * 

def refreshpodioaccesstoken():
    payload = {'grant_type': 'refresh_token', 'client_id': '%s' % (client_id,), 'client_secret': '%s' % (client_secret,), 'refresh_token': '%s' % (refresh_token,)}
    response = requests.post("https://podio.com/oauth/token", data=payload)
    data = response
    res = data.json()
    print res['access_token']
    return res['access_token']

def podiocontactsfetch(accesstoken):    
    response = requests.get('https://api.podio.com/item/app/%s/' % (app_id,), headers={'Authorization': 'OAuth2 %s' % (accesstoken,)})
    data = response
    res = data.json()
    return res
    
def podiocontacts():
    res = podiocontactsfetch(accesstoken)
    if 'error' in res.keys():
        print "access token expired"
        access_token = refreshpodioaccesstoken()
        res = podiocontactsfetch(access_token)
    
    for key,value in res.items():
        if key=="items":
            for l in value: 
                for k,v in l.items():
                    if k == "fields":
                        for ite in v:
                            for x,y in ite.items():
                                if x =="external_id" and y=="title":
                                    print "Name: ", ite['values'][0]['value']
                                if x =="external_id" and y =="email-address":
                                    print "email-id", ite['values'][0]['value']
                                if x =="external_id" and y=="monthly-billable-amount":
                                    print "Monthly-billable-amount: ", ite['values'][0]['value']
                                if x =="external_id" and y=="status":
                                    print "status: ", ite['values'][0]['value']['text']
                                    print
                                
podiocontacts()
