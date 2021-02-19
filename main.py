import sys
from clone import clone
from src.infrastructure.aid import get_folder_to_clone_label, get_folder_to_search_label, get_word_to_search_label, \
    default_f_to_search, default_w_to_search
import getpass
from search import search

if __name__ == '__main__':
    # variables to clone script
    username = input(f'Username*: ')
    if username is None or len(username) == 0:
        print(f'You must insert the username')
        sys.exit(-1)
    password = getpass.getpass(f'Password*: ')
    if password is None or len(password) == 0:
        print(f'You must insert the password')
        sys.exit(-1)
    destiny = input(get_folder_to_clone_label())
    destiny = default_f_to_search if (destiny is None or len(destiny) == 0) else destiny
    # variables to search script
    f_to_find = input(get_folder_to_search_label(destiny))
    f_to_find = destiny if (f_to_find is None or len(f_to_find) == 0) else f_to_find
    w_to_find = input(get_word_to_search_label())
    w_to_find = default_w_to_search if (w_to_find is None or len(w_to_find) == 0) else w_to_find
    clone(username, password, destiny, False)
    search(f_to_find, w_to_find, False)
    print(f'All done ;)')
    sys.exit(-1)