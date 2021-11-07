#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 15:15:07 2021

@author: rluisfue
"""
from EC601Project2ProductV2 import *

def test_getBearerToken():
    bearer = ""
    bearer = getBearerToken()
    assert(len(bearer) > 1)

    
def test_getUserID():
    userId = ""
    userId = getUserID("BUCollegeofENG",getBearerToken())
    assert(len(userId) > 1)

        
def test_getSentiment():
    negative = "\"I am a terrible programmer and am no better than a mangy dog.\""
    negativeSentiment = ""
    negativeSentiment = getSentiment(negative)
    assert(len(negativeSentiment) > 1)

    positive = "\"I am a fantastic programmer and will do great things with my talents.\""
    positiveSentiment = ""
    positiveSentiment = getSentiment(positive)
    assert(len(positiveSentiment) > 1)

def test_getTweets():
    print("Testing search of tweets for the @BUCollegeofENG account")
    tweets = getTweets(getBearerToken(),'94150521',0,0,True)
    tweetCount = 0
    if "data" in tweets:  
        tweetCount = len(tweets["data"])
        assert(tweetCount > 0)
    else:
        raise Exception("No tweets found")
        