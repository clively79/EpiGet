import sys

import json
from bs4 import BeautifulSoup
import configuration

import epigetmodules


def main():
    argCalls = {
        '--add': epigetmodules.addShowToSchedule,
        '--del': epigetmodules.deleteShowFromSchedule,
        '--help': epigetmodules.printUsage
    }

    try:
        argCalls[sys.argv[1]]()
    except:
        print(
            f'unknown argument \'{sys.argv[1]}\' was not recognized.  Run EpiGet --help for list of arguments.')


"""
    

    candidates = findBestMatch(data, showdetails)
    if len(candidates) == 0:
        print("No candidates found!")
    for i, entry in enumerate(candidates):
        print(
            f"[{i}] Summary: {entry['show']['name']}\n\t{detag(entry['show']['summary'])}")
        promptResponse = input("Schedule this show for Download? (Y/n): ")
        while True:
            if promptResponse.lower() in ['y', 'n', 'yes', 'no', '']:
                break
            else:
                print(f'\"{promptResponse}\": Was not understood.')
                print(
                    f"[{i}] Summary: {entry['show']['name']}\n\t{detag(entry['show']['summary'])}")
                continue

        if promptResponse.lower() in ['y', 'yes', '']:
            addShowToSchedule(entry)
            break
        else:
            continue """


def detag(s):
    soup = BeautifulSoup(s, 'html.parser')

    for data in soup(['style', 'script']):
        data.decompose()

    return ' '.join(soup.stripped_strings)


def findBestMatch(data, target):
    i = 0
    for entry in data:
        while(len(data) > i):
            if target['title'].lower() != data[i]['show']['name'].lower():
                del data[i]
                continue
            if target['year'] == '':
                break
            elif target['year'] != str(data[i]['show']['premiered']).split('-')[0]:
                del data[i]
                continue
            if target['studio'] == '':
                break
            elif data[i]['show']['network'] != None:
                if str(target['studio']).lower() not in str(data[i]['show']['network']['name']).lower().split(' '):
                    del data[i]
                    continue
            elif str(target['studio']).lower() != str(data[i]['show']['webChannel']['name']).lower():
                del data[i]
                continue
            i += 1
        i += 1

    return data


def populateShowDetails(dict):
    i = 1
    for x in dict:
        if i == len(sys.argv):
            break
        dict[x] = sys.argv[i]
        i += 1


if __name__ == "__main__":
    if (len(sys.argv)) < 2:
        print("NextAirDate requires at least one argument.")
    elif (sys.argv[1] == '--configure'):
        epigetmodules.configure()
    else:
        try:
            global settings
            settings = open('config.json', 'r')
        except:
            print(
                "EpiGet has not been configured. Run 'epiget.py --configure' before using EpiGet.")
        else:
            log = open('EpiGet.log', 'a')
            configfile = open('config.json', 'r')
            config = configuration.configs(json.loads(configfile.read()))
            configfile.close()
            main()
            log.close()
