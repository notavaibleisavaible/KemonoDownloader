import os
import sys
import config
import download


PLATFORM_DICT = {0: 'patreon', 1: 'fanbox', 2: 'discord', 3: 'fantia', 4: 'afdian', 5: 'boosty', 6: 'dlsite', 7: 'gumroad', 8: 'subscribestar'}

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


class Session:
    def __init__(self):
        try:
            os.mkdir(f'{config.DOWNLOAD_DIR}cache/')
        except FileExistsError:
            pass
        except:
            sys.exit(f'{TERMINAL.RED}ERROR: Could not create {config.DOWNLOAD_DIR}{TERMINAL.NONE}')
        TERMINAL.clear()
        self.CREATOR_ID = input(f'{TERMINAL.GREEN}{TERMINAL.BOLD}Creator ID\n > {TERMINAL.NONE}')
        self.CREATOR_PLAT = PLATFORM_DICT[int(input(f'{TERMINAL.YELLOW}Platform:\n0 - patreon | 1 - pixiv fanbox | 2 - discord | 3 - fantia | 4 - afdian | 5 - boosty | 6 - dlsite | 7 - gumroad | 8 - subscribestar\n > {TERMINAL.NONE}'))]
        TERMINAL.clear()
        print(f'{TERMINAL.BLUE}{TERMINAL.BOLD}Creator ID: {self.CREATOR_ID} - {self.CREATOR_PLAT}{TERMINAL.NONE}')
        print(f'{TERMINAL.BOLD}Download Dir: {config.DOWNLOAD_DIR}{self.CREATOR_ID}{TERMINAL.NONE}')
        input(f'Press anything to continue...')
        try:
            os.mkdir(f'{config.DOWNLOAD_DIR}{self.CREATOR_ID}')
        except FileExistsError:
            pass
        except:
            sys.exit(f'{TERMINAL.RED}ERROR: Could not create {config.DOWNLOAD_DIR}{self.CREATOR_ID}{TERMINAL.NONE}')
        download.Download(self.CREATOR_ID, self.CREATOR_PLAT)
        
    

Session()
