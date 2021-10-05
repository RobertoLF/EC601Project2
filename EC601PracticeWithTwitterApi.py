# -*- coding: utf-8 -*-
"""
Dev: Roberto Luis-Fuentes
Boston University 
U38239113
"""
import requests 

interrupt = 'Y'
firstime =  1
import base64
import datetime

def getBearerToken():
    URL = "https://api.twitter.com/oauth2/token"
    parameter = {'grant_type':"client_credentials"}
    accessTokenFile = open(r"/Users/rluisfue/.spyder-py3/EC601/AcessToken.txt")
    secretFile = open(r"/Users/rluisfue/.spyder-py3/EC601/AccessTokenSecret.txt")
    accessToken = accessTokenFile.read()
    secret = secretFile.read()
    authenticator = accessToken + ':' + secret
    autheticatorBytes = authenticator.encode('ascii')
    b64Bytes = base64.b64encode(autheticatorBytes)
    b64Authenticator = b64Bytes.decode('ascii')
    header = {'Host':"api.twitter.com",'User-Agent':"22055381",'Authorization':"Basic " + b64Authenticator,
              'Content-Type':"application/x-www-form-urlencoded;charset=UTF-8",'Accept-Encoding':"gzip"}
    r = requests.post(url=URL, headers=header, data = parameter)
    inspect=r.json()
    return inspect["access_token"]

queryStart = ""
queryEnd = ""
startTimeError = 0
errors = {"":""}
params = {"":""}
saveResults = "N"
def getMentions(token,userId,nextToken,getDate):
    URL = "https://api.twitter.com/2/users/" + userId + "/mentions"
    if getDate == 1:
        start = input(""""Please enter a start date past 2011-01-01 to determine the oldest timestamp
  from which mentions will be provided in the format 'YYYY-MM-DD':""")
        year = int(start[0:4])
        if year < 2011:
            print("An invalid start date was entered!")
            global startTimeError
            startTimeError = 1
            return {"":""}
        global queryStart
        queryStart = start + "T00:00:01-04:00"
        global queryEnd
        queryEnd = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()
    parameters = {'max_results':"100",'start_time':queryStart,'end_time':queryEnd}
    if nextToken != 0:
        parameters["pagination_token"] = nextToken
    headers = {'Authorization':"Bearer " + token}
    r = requests.get(url=URL,params=parameters,headers=headers)
    inspect = r.json() 
    global errors
    global params
    if "errors" in inspect:
        errorList = inspect["errors"]
        errors = errorList[0]
    if "parameters" in errors:
        params = errors["parameters"]
    if "start_time" in params:
        startTimeError = 1
        print("The entered start date was invalid")
    return inspect 

while (interrupt == 'Y'):
    if firstime == 1:
        print("Hello!")
        print("""This program searches twitter for all the mentions of a twitter handle 
 given a start date. The maximum number of mentions this program can find is 700.""")
        
    handle = input("Enter a twitter handle to search mentions for: ")
    token = getBearerToken()
    URL = "https://api.twitter.com/2/users/by/username/" + handle
    header = {'Authorization':"Bearer " + token}
    r = requests.get(url=URL, headers=header)
    userData = r.json()
    userID = ""
    if "errors" in userData:
        print("Twitter handle not found!")
    else:
        userID = userData["data"]["id"]
    nextToken = 0
    tweetCount= 0
    getDate = 1
    skip = 0
    mentions  = {}
    while nextToken != 1 and userID != "" and startTimeError == 0:
        mentions.update(getMentions(token, userID,nextToken,getDate))
        if startTimeError == 0:
            meta = mentions["meta"]
            tweetCount += len(mentions["data"])
            if "next_token" in meta:
                nextToken = meta["next_token"]
            else:
                nextToken =1
            getDate = 0
        if tweetCount > 800:
            print("""We found  %d mentions for the %s handle between the dates of %s & %s.
  That is the limit of tweets this program can access!""" %(tweetCount,handle,queryStart,queryEnd))
            skip = 1
            saveResults = input("Would you like to save your results?(Y/N): ")
                  
    if userID != "" and startTimeError == 0 and skip == 0:    
        print("""
We found %d mentions for the %s handle between the dates of %s & %s.""" %(tweetCount,handle,queryStart,queryEnd))     
        saveResults = input("Would you like to save your results?(Y/N): ")
        
    if saveResults == "Y":
       fileToSave = open(handle + "_" + queryStart + ".txt","w")
       fileToSave.write(str(mentions))
       fileToSave.close()
       print(" ")
       print("Mentions were saved to the file "+handle+"_"+queryStart+".txt"+" in this programs root directory" )
    interrupt = input("Would you like to try again? (Y/N): ")
    firstime = 0
    startTimeError = 0
    errors = {}
    params = {}
    mentions = {}



