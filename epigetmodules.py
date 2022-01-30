import sys
import json
import datetime
import configuration
import requests
from bs4 import BeautifulSoup


def addShowToSchedule():

    if '-t' not in sys.argv:
        raise('Arguments must include a title')

    sys.argv.pop(1)

    showdetails = {
        'title': '',
        'year': '',
        'studio': ''
    }

    optionalFunctions = {
        '-t': lambda a: showdetails['title'] + a,
        '-y': lambda a: showdetails['year'] + a,
        '-n': lambda a: showdetails['year'] + a
    }
    while len(sys.argv) > 1:
        optionalFunctions[sys.argv.pop(1)](sys.argv.pop(1))

    data = scrape(showdetails['title'])


def scrape(title):
    url = "https://tvjan-tvmaze-v1.p.rapidapi.com/search/shows"
    querystring = {"q": title}
    headers = {
        'x-rapidapi-host': "tvjan-tvmaze-v1.p.rapidapi.com",
        'x-rapidapi-key': config.api_key
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    log.write(
        f"[{datetime.datetime.now()}] API query: \'{title}\' initiated.  Result code: {response.status_code}\n")
    showData = json.loads(response.text)
    return showData


def deleteShowFromSchedule():
    print('You\'ve asked to remove a show from the schedule')


def printUsage():
    print('You\'ve asked to see the usage')


def configure():
    import os
    if 'help' in sys.argv:
        file = open('confighelp', 'r')
        print(file.read())
        file.close()

    configuration = {
        'ver': 0.01,
        'API-Key': '',
        'library-path': '',
        'torrent-path': '',
        'download-path': ''
    }

    for key in configuration:
        if key == 'ver':
            continue
        temp = input(f'{key}: ')

        if key == 'API-Key':
            configuration[f'{key}'] = temp
            continue
        try:
            configuration[f'{key}'] = temp + '\\' if temp[-1] != '\\' else temp
            open(configuration[f'{key}'] + 'test.conf', 'w')
        except:
            print('Unable to write to path provided. Verify that EpiGet has permission to write to the specified directory and rerun configuration')
        else:
            os.remove(configuration[f'{key}']+'test.conf')

        configfile = open('config.json', 'w')
        configfile.write(json.dumps(configuration, indent=4))
        configfile.close()
