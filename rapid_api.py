import requests

url = "https://api-football-v1.p.rapidapi.com/v3/standings"

querystring = {"season":"2021","team":"33"}

headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "9844a989b8msh640764f7724a65bp12b89fjsn81ba0d5064ea"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)