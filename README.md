# Digital_Twins

This repository contains code developed for a university project at the University of Leoben, Austria. With the code provided, it is possible to build a Digital Twin of a 
football (soccer) club and analyze the number of tweets posted containing keywords defined in the Excel-Sheet keywords_definition.xls during matches or in a time range, the 
development of the club's stock price and the influence of matches on it and how Google searches evolves for certain keywords concerning the club. 

## twitter_data.py
This script downloads the number of tweets per minute for the last 7 days for every keyword defined in keywords_definition.xls.

## Plot Handler
Does the plotting of the data.

## Twitter Handler
Handles the twitter data so that Plot Handler can plot it.

## Match Handler
Handles the manually compiled match data so that Plot Handler can plot it. 

## Google Trends Handler
Given keywords, Google Trends Handler loads and returns the number of Google searches.
