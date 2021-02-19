import os

default_w_to_search = 'staticfiles'
default_f_to_search = os.path.abspath('.')
repositories_file = './repositories.csv'


def get_folder_to_clone_label(default=default_f_to_search):
    return f"Insert the Folder to clone (default '" + default + "'): "


def get_folder_to_search_label(default=default_f_to_search):
    return f"Insert the Folder to search (default '" + default + "'): "


def get_word_to_search_label(default=default_w_to_search):
    return "Insert the Word to find (default '" + default + "'): "


