import requests
import os
import config
import json
import ast
import wget
import sys

API_URL = 'https://kemono.party/api/v1/'
DOWNLOAD_URL = 'https://c1.kemono.su/data'
NumberOfFiles = 0



class COLORS:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    none = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear():
    os.system('cls' if os.name=='nt' else 'clear')


def main():
    global CREATOR_ID
    global CREATOR_PLAT
    clear()
    CREATOR_ID = input(f'{COLORS.GREEN}{COLORS.BOLD}Creator ID\n > {COLORS.none}')
    CREATOR_PLAT = input(f'{COLORS.YELLOW}Platform:\n0 - patreon | 1 - pixiv fanbox | 2 - discord | 3 - fantia | 4 - afdian | 5 - boosty | 6 - dlsite | 7 - gumroad | 8 - subscribestar\n > {COLORS.none}')
    clear()
    print(f'{COLORS.BLUE}Creator ID: {CREATOR_ID} - {getPlatform(CREATOR_PLAT)}{COLORS.none}')
    print(f'{COLORS.BOLD}Download Dir: {config.DOWNLOAD_DIR}{COLORS.none}')

    
    print(f'{COLORS.BOLD}Type {COLORS.GREEN}{COLORS.none}\'S\' To start or something else to cancel{COLORS.none}')
    match input():
        case 's':
            startDownload(CREATOR_ID, CREATOR_PLAT, config.DOWNLOAD_DIR)
        case 'S':
            startDownload(CREATOR_ID, CREATOR_PLAT, config.DOWNLOAD_DIR)
        case _:
            quit()












def getPlatform (PLATFORM):
    try:
        PLATFORM = int(PLATFORM)
    except:
        return 'Not A Number'
        quit()

    match PLATFORM:
        case 0:
            return 'patreon'
        case 1:
            return 'fanbox'
        case 2:
            return 'discord'
        case 3:
            return 'fantia'
        case 4:
            return 'afdian'
        case 5:
            return 'boosty'
        case 6:
            return 'dlsite'
        case 7:
            return 'gumroad'
        case 8:
            return 'subscribestar'
        
        case _:
            return 'ERROR: bad platform!'
            quit()

def delete_last_line():
    sys.stdout.write('\x1b[1A')
    #sys.stdout.write('\x1b[2K')


def getCreatorPosts(user, plat):
    url = f'{API_URL}{getPlatform(plat)}/user/{user}/'
    response = requests.get(url)
    try:
        os.mkdir(f'{config.DOWNLOAD_DIR}cache/')
    except:
        pass
    with open(f'{config.DOWNLOAD_DIR}cache/posts.json', 'w') as f:
        f.write(response.text)


def getContentLink():
    CONTENT_ID = []
    json_data_list = []
    with open(f'{config.DOWNLOAD_DIR}cache/posts.json') as f:
     json_data_list = json.load(f)

    for i in json_data_list:
        for j in (i['attachments']):
            CONTENT_ID.append(j['path'])

    with open(f'{config.DOWNLOAD_DIR}cache/content_links.txt', 'w') as f:
      f.write(str(CONTENT_ID))

def Counter():
    global NumberOfFiles
    NumberOfFiles = NumberOfFiles +1

def download(link):
    link_title = link.rsplit('/', 1)[-1]
    delete_last_line()
    print(f'\n{COLORS.GREEN}[Download] Started {COLORS.BOLD}{COLORS.BLUE}{link_title}{COLORS.none}                                  ')
    wget.download(link, f'{CREATOR_FOLDER}')
    Counter()


def downloadHelper():
    with open(f'{config.DOWNLOAD_DIR}cache/content_links.txt', 'r') as f:
        link_dict = []
        link_dict = f.read()
        link_dict = ast.literal_eval(link_dict)
    for i in link_dict:
        download(f'{DOWNLOAD_URL}{i}')
    print(f'\n{COLORS.BOLD}{COLORS.PINK}Download Done!{COLORS.none}{COLORS.YELLOW}{COLORS.BOLD} [{NumberOfFiles}]{COLORS.none}{COLORS.PINK} Files Downloaded{COLORS.none}')
    quit()


def startDownload(CREATOR, PLATFORM, DIR):
    global CREATOR_FOLDER
    CREATOR_FOLDER = f'{config.DOWNLOAD_DIR}{CREATOR}/'
    getCreatorPosts(CREATOR_ID, CREATOR_PLAT)
    getContentLink()
    try:
        os.mkdir(CREATOR_FOLDER)
    
    except FileExistsError:
        pass
    except Exception as e:
        print(f'{COLORS.RED}Error: Could Not Create Directory: {CREATOR_FOLDER}{COLORS.none}')
        print(e)
        quit()
    downloadHelper()






main()