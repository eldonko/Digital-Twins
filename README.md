# Digital_Twins

This repository contains code developed for a university project at the University of Leoben, Austria. With the code provided, it is possible to build a Digital Twin of a 
football (soccer) club and analyze the number of tweets posted containing keywords defined in the Excel-Sheet Keyword_definition.xls during matches or in a time range, the 
development of the club's stock price and the influence of matches on it and how Google searches evolves for certain keywords concerning the club. 

## twitter_data.py
This script downloads the number of tweets per minute for the last 7 days for every keyword defined in keywords_definition.xls. The data is then stored in one single csv-File for every keyword. Locally storing the data is necessary as the Twitter API only allows access to data from the last 7 days. To make use of this script, a personal bearer token needs to be retrieved from the Twitter API. 

## Twitter Handler
For a given list of keywords, Twitter Handler loads the data obtained by twitter_data.py using the pandas framework. It is possible to analyze the data during a match or in a time range. If the analysis is to be done for a single match, the match data needs to be provided in an Excel worksheet. An exemplary version of match data might be provided  here in the future. 

## Match Handler
Given an Excel worksheet containing events that happened during a match (an exemplary version might be provided here in the future), Match Handler can load this information and return it in a pandas DataFrame. 

## Google Trends Handler
Given keywords, Google Trends Handler loads and returns the number of Google searches.

## Plot Handler
Does the plotting of the data.
