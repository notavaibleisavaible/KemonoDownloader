import config
import requests
import sys
import time
import json
import wget
import threading
import ast
import os

API_URL = 'https://kemono.party/api/v1/'
DOWNLOAD_URL = 'https://c1.kemono.su/data'


class TERMINAL:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    NONE = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def clear():
        os.system('cls' if os.name=='nt' else 'clear')

class Download:
        def __init__(self, CREATOR_ID, CREATOR_PLAT):
            self.CREATOR_ID = CREATOR_ID
            self.CREATOR_PLAT = CREATOR_PLAT
            self.DOWNLOAD_FOLDER = f'{config.DOWNLOAD_DIR}{self.CREATOR_ID}'
            self.AMMOUNT_OF_FILES_DOWNLOADED = 0
            self.CURRENT_THREADS = 0
            self.MAX_THREADS = config.MAX_THREADS
            self.StartDownload(self.CREATOR_ID, self.CREATOR_PLAT)
    
        def UpdateTerminal(self):
            TERMINAL.clear()
            print(f'{TERMINAL.BLUE}{TERMINAL.BOLD}Creator ID: {self.CREATOR_ID} - {self.CREATOR_PLAT}{TERMINAL.NONE}')
            print(f'{TERMINAL.BOLD}Download Dir: {config.DOWNLOAD_DIR}{self.CREATOR_ID}{TERMINAL.NONE}')
            print(f'{TERMINAL.BOLD}{TERMINAL.GREEN}[Info] {TERMINAL.NONE}Successfully downloaded {TERMINAL.BOLD}{TERMINAL.BLUE}{self.AMMOUNT_OF_FILES_DOWNLOADED}/{self.AMMOUNT_OF_FILES}{TERMINAL.NONE}')



        def AmmountOfPages(self, CREATOR_ID, CREATOR_PLAT):
            i = 0
            while True:
                URL = f'{API_URL}{CREATOR_PLAT}/user/{CREATOR_ID}?o={i}'
                response = requests.get(URL, params='')
                if len(response.text) < 3:  # size of '[]' + 1 (response from the server if empty)
                    return i - 50
                    break
                else: 
                    pass
                time.sleep(0.1)
                i = i + 50

        def PostsExtractor(self, CREATOR_ID, CREATOR_PLAT):
            print(f'{TERMINAL.GREEN}Started post extraction...{TERMINAL.NONE}')
            self.CREATOR_ID = CREATOR_ID
            self.CREATOR_PLAT = CREATOR_PLAT            
            self.AMMOUNT_OF_PAGES = self.AmmountOfPages(self.CREATOR_ID, self.CREATOR_PLAT) 
            self.URL = f'{API_URL}{self.CREATOR_PLAT}/user/{self.CREATOR_ID}?o='
            self.CONTENT_ID = []
            self.LOOPS = self.AMMOUNT_OF_PAGES / 50          
            i = 0
            while i <= self.LOOPS:
                p = i * 50
                response = requests.get(f'{self.URL}{p}', params= '')
                with open(f'{config.DOWNLOAD_DIR}cache/raw.json', 'w') as f:
                    f.write(response.text)
                with open(f'{config.DOWNLOAD_DIR}cache/raw.json') as f:
                    json_data_list = json.load(f)
                
                for k in json_data_list:
                    for j in (k['attachments']):
                        self.CONTENT_ID.append(j['path'])
                for m in json_data_list:
                    try:
                        self.CONTENT_ID.append(m['file']['path'])
                    except:
                        pass
                i = i + 1

            with open(f'{config.DOWNLOAD_DIR}cache/links.txt', 'w') as f:
                f.write(str(self.CONTENT_ID))
            return(len(self.CONTENT_ID)) #returns the ammount of files to be downloaded


        def Threader(self, LINK):
            def download(LINK):
                wget.download(LINK, f'{config.DOWNLOAD_DIR}{self.CREATOR_ID}', bar=None)
                self.CURRENT_THREADS = self.CURRENT_THREADS - 1
                self.AMMOUNT_OF_FILES_DOWNLOADED = self.AMMOUNT_OF_FILES_DOWNLOADED + 1
                self.UpdateTerminal()

            threading.Thread(target=download, args=[f'{DOWNLOAD_URL}{LINK}']).start()



        def StartDownload(self, CREATOR_ID, CREATOR_PLAT):   
            self.CREATOR_ID = CREATOR_ID
            self.CREATOR_PLAT = CREATOR_PLAT
            self.CREATOR_URL = f'{API_URL}{self.CREATOR_PLAT}/user/{self.CREATOR_ID}'
            self.AMMOUNT_OF_FILES = self.PostsExtractor(self.CREATOR_ID, self.CREATOR_PLAT)

            self.LINK_LIST = []
            with open(f'{config.DOWNLOAD_DIR}cache/links.txt') as f:
                self.LINK_LIST = f.read()
                self.LINK_LIST = ast.literal_eval(self.LINK_LIST)

                for y in self.LINK_LIST:
                    while True:
                        if self.CURRENT_THREADS < self.MAX_THREADS:
                            self.Threader(y)
                            self.CURRENT_THREADS = self.CURRENT_THREADS + 1
                            break
                        else:
                            time.sleep(0.01)
        
            self.UpdateTerminal()