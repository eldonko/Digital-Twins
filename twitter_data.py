import requests
import os
import json
import pandas as pd
import datetime

bearer_token = "ENTER_TOKEN_HERE"
search_url = "https://api.twitter.com/2/tweets/counts/recent"


def main():
    # Get number of tweets per keywords
    keywords = get_keywords()
    search_twitter(keywords)


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentTweetCountsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def get_keywords():
    """
    Loads the keywords for the twitter search
    :return: list of keywords
    """

    keyword_file = r"C:\Users\danie\Documents\Montanuni\2021_22WS\Digital Twins\3 Code\Keyword_definition.xls"
    keywords_df = pd.read_excel(keyword_file)

    return list(keywords_df['Keyword'])


def write_csv(response, filename):
    """
    Writes the findings to a csv file
    :param response: json_response
    :param filename: the file to save the data in
    :return:
    """

    df = pd.DataFrame(response['data'])
    df.to_csv(filename, mode='a')


def query_tweets(keyword, filename, granularity='minute', next_token=None):
    """

    :param keyword: The keyword to search for in twitter data
    :param filename: The filename to store the data
    :param next_token: If the last query was too long, a next_token is returned to be able
    to continue searching at the point the last search left off.
    :param granularity: the granularity of the search
    :return: The json response and, if existing, the next_token
    """

    # Define the query
    query_params = {'query': keyword, 'granularity': granularity}
    if next_token is not None:
        query_params = {'query': keyword, 'granularity': granularity, 'next_token': next_token}

    # Get the json response
    json_response = connect_to_endpoint(search_url, query_params)

    # Write the data to the keyword search csv
    write_csv(json_response, filename)

    # Presume the query if there is a next_token
    if 'next_token' in json_response['meta']:
        query_tweets(keyword, filename=filename, granularity=granularity,
                     next_token=json_response['meta']['next_token'])


def get_timestamp():
    """
    Return the current date as a string
    :return: timestamp as string in the format DD-MM-YYYY_hour_minute_second
    """

    time_now = datetime.datetime.now()

    day = time_now.day
    month = time_now.month
    year = time_now.year
    hour = time_now.hour
    minute = time_now.minute
    second = time_now.second

    return str(day) + '-' + str(month) + '-' + str(year) + '_' + str(hour) \
           + '_' + str(minute) + '_' + str(second)


def search_twitter(keywords):
    # Loop through all the keywords and get all the data (start a new query with next token to
    # resume where the last search left off)
    for i, keyword in enumerate(keywords):
        print(str(i + 1) + '/' + str(len(keywords)))
        granularity = 'minute'
        filename = '..\\4 Data\\' + keyword + '_' + granularity + '_' + get_timestamp() + '.csv'
        # If tweets by one account are looked up, the keyword contains a :. :s in filename give
        # corrupted files, therefore the : will be replaced by an _ in this case
        if ':' in keyword:
            key = keyword.replace(':', '_')
            filename = '..\\4 Data\\' + key + '_' + granularity + '_' + get_timestamp() + '.csv'

        query_tweets(keyword=keyword, filename=filename, granularity=granularity)


if __name__ == "__main__":
    main()
