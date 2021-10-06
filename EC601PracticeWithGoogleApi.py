#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dev: Roberto Luis-Fuentes
Boston University 
U38239113
"""




from google.cloud import language_v1
import os 

filePath = input("""Please enter the path to a text file you would like this app to analyze
the sentiment for: """)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/rluisfue/Documents/ec601-327314-c0d53011a952.json"

client = language_v1.LanguageServiceClient()

file = open(filePath,"r")
textToAnalyze = file.read()

googleDocument = language_v1.Document(content=textToAnalyze, type_=language_v1.Document.Type.PLAIN_TEXT)
sentiment = client.analyze_sentiment(request={'document':googleDocument}).document_sentiment

score = sentiment.score

if score < -0.75 :
    print("The sentiment of the input document is nearly entirely negative! :(")
elif score < -0.5 and score > -0.75 :
    print("The sentiment of the input document is very negative.")
elif score < -0.25 and score > -0.5 :
    print("The sentiment of the input document is negative.")
elif score < 0 and score > -0.25 : 
    print("The sentiment of the input document is slightly negative and nearly neutral.")
elif score == 0 :
    print("The sentiment of the input document is neutral. :|")
elif score > 0 and score < 0.25:
    print("The sentiment of the input document is slightly positive and nearly neutral.")
elif score > 0.25 and score < 0.5 :
    print("The sentiment of the input document is negative.")
elif score > 0.5 and score < 0.75 :
    print("The sentiment of the input document is very positive.")
elif score > 0.75:
    print("The sentiment of the input document is nearly entirely positive! :)")