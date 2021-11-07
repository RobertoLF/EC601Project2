# -*- coding: utf-8 -*-
"""
Dev: Roberto Luis-Fuentes
Boston University 
U38239113
"""
import requests 
import base64
from google.cloud import language_v1
import os 

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ec601-327314-c0d53011a952.json"
client = language_v1.LanguageServiceClient()
start = ""
end = ""
queryStart = ""
queryEnd = ""
TimeError = 0
errors = {"":""}

def getBearerToken():
    bearerURL = "https://api.twitter.com/oauth2/token"
    parameter = {'grant_type':"client_credentials"}
    accessToken = os.environ.get('TWITTER_ACCESS_TOKEN')
    secret = os.environ.get('TWITTER_SECRET')
    authenticator = accessToken + ':' + secret
    autheticatorBytes = authenticator.encode('ascii')
    b64Bytes = base64.b64encode(autheticatorBytes)
    b64Authenticator = b64Bytes.decode('ascii')
    header = {'Host':"api.twitter.com",'User-Agent':"22055381",'Authorization':"Basic " + b64Authenticator,
              'Content-Type':"application/x-www-form-urlencoded;charset=UTF-8",'Accept-Encoding':"gzip"}
    r = requests.post(url=bearerURL, headers=header, data = parameter)
    inspect=r.json()
    return inspect["access_token"]

def getTweets(token,userId,nextToken,getDate,testMode):
    mentionsURL = "https://api.twitter.com/2/users/" + userId + "/tweets"
    if getDate == 1:
        global start
        start = input(""""Please enter a start date past 2011-01-01 to determine the oldest timestamp
from which tweets will be provided in the format 'YYYY-MM-DD':""")
        global end
        end = input(""""Please enter an end date past your start date to determine the newest timestamp
from which tweets will be provided in the format 'YYYY-MM-DD':""")
        print("\n")
        startYear = int(start[0:4])
        if startYear < 2011:
            print("An invalid start date was entered!\n")
            global TimeError
            TimeError = 1
        endYear = int(end[0:4])
        if startYear > endYear:
            print("An invalid end date was entered!\n")
            TimeError = 1
        global queryStart
        queryStart = start + "T00:00:01-04:00"
        global queryEnd
        queryEnd = end + "T00:00:01-04:00"
    if testMode == True:
        parameters = {'max_results':100}
    else:
        parameters = {'max_results':100,'start_time':queryStart,'end_time':queryEnd}
    if nextToken != 0:
        parameters["pagination_token"] = nextToken
    headers = {'Authorization':"Bearer " + token}
    r = requests.get(url=mentionsURL,params=parameters,headers=headers)
    inspect = r.json() 
    global errors
    params = {}
    if "errors" in inspect:
        errorList = inspect["errors"]
        errors = errorList[0]
    if "parameters" in errors:
        params = errors["parameters"]
    if "start_time" in params:
        TimeError = 1
        print("The entered start date was invalid\n")
    if "end_time" in params:
        TimeError = 1
        print("The entered end date was invalid\n")
    return inspect 

def getUserID(handle,token):
    usernameURL = "https://api.twitter.com/2/users/by/username/" + handle
    header = {'Authorization':"Bearer " + token}
    r = requests.get(url=usernameURL, headers=header)
    userData = r.json()
    userID = ""
    if "errors" in userData:
        print("Twitter handle not found! \n")
    else:
        userID = userData["data"]["id"]
    return userID

def getSentiment(textToAnalyze):
    googleDocument = language_v1.Document(content=textToAnalyze, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={'document':googleDocument}).document_sentiment
    score = sentiment.score
    translation = ""
    if score < -0.75 :
        translation = "The sentiment of the found tweets is nearly entirely negative! :( \n"
    elif score < -0.5 and score > -0.75 :
        translation = "The sentiment of the found tweets is very negative. \n "
    elif score < -0.25 and score > -0.5 :
        translation = "The sentiment of the found tweets is negative. \n"
    elif score < 0 and score > -0.25 : 
        translation = "The sentiment of the found tweets is slightly negative and nearly neutral. \n"
    elif score == 0 :
        translation = "The sentiment of the found tweets is neutral. :| \n"
    elif score > 0 and score < 0.25:
        translation = "The sentiment of the found tweets is slightly positive and nearly neutral. \n"
    elif score > 0.25 and score < 0.5 :
        translation = "The sentiment of the found tweets is negative. \n"
    elif score > 0.5 and score < 0.75 :
        translation = "The sentiment of the found tweets is very positive. \n"
    elif score > 0.75:
        translation = "The sentiment of the found tweets is nearly entirely positive! :) \n"
    return translation

def main():
    interrupt = 'Y'
    firstime =  1
    global start
    global end
    global TimeError
    global errors
    while (interrupt == 'Y'):
        if firstime == 1:
            print("Hello!\n")
            print("""This program searches twitter for all the tweets of a specified user
given a start/end date and subsequently determines the sentiment of the found tweets.
The maximum number of Tweets this program can find is 3200. \n""")
            
        handle = input("Enter a twitter handle to search tweets for: ")
        print("\n")
        token = getBearerToken()
        userID = getUserID(handle,token)
        nextToken = 0
        tweetCount= 0
        getDate = 1
        skip = 0
        tweets  = {}
        while nextToken != 1 and userID != "" and TimeError == 0:
            tweets.update(getTweets(token,userID,nextToken,getDate,False))
            if TimeError == 0:
                if "meta" in tweets:
                    meta = tweets["meta"]
                if "data" in tweets:  
                    tweetCount += len(tweets["data"])
                if "next_token" in meta:
                    nextToken = meta["next_token"]
                else:
                    nextToken =1
                getDate = 0
            if tweetCount > 3200:
                print("""Found  %d tweets for the %s handle between the dates of %s & %s.
That is the limit of tweets this program can access! \n""" %(tweetCount,handle,start,end))
                skip = 1
                 
        if userID != "" and TimeError == 0 and skip == 0:    
            print("Found %d tweets for the %s handle between the dates of %s & %s. \n" %(tweetCount,handle,start,end))     
    
        if tweetCount > 0:
            textToAnalyze = ""
            for x in tweets['data']:
                textToAnalyze = textToAnalyze + x['text'] + "\n"
            sentimentAnalysis = getSentiment(textToAnalyze)
            print(sentimentAnalysis)
            
        interrupt = input("Would you like to try again? (Y/N): ")
        print('\n')
        firstime = 0
        TimeError = 0
        errors = {}
        tweets = {}
        
if __name__ == "__main__":
    main()