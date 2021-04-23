import os

keyword = 'arquivosestaticos'
default_w_to_search = keyword
default_f_to_search = os.path.abspath('')
repositories_file = './repositories.csv'


def get_folder_to_clone_label(default=default_f_to_search):
    return f"Insert the Folder to clone (default '" + default + "'): "


def get_folder_to_search_label(default=default_f_to_search):
    return f"Insert the Folder to search (default '" + default + "'): "


def get_word_to_search_label(default=default_w_to_search):
    return "Insert the Word to find (default '" + default + "'): "


def to_string(inn):
    if inn is not None and len(str(inn)) > 0:
        return (str(inn)).strip().rstrip()
    else:
        return ''


def remove_semicolon(inn):
    return inn.replace(';', '')


# from migration bound
proxies = {
'http': 'http://proxyad.itau/accelerated_pac_base.pac:8080',
'https': 'http://proxyad.itau/accelerated_pac_base.pac:443'
}

default_f_to_read = os.path.abspath('') + '/results.csv'


def get_file_to_read_label(default=default_f_to_read):
    return f"Insert the file path to read and download references (default '" + default + "'): "


default_column_of_the_urls = 0


def get_column_of_the_urls_label(default=default_column_of_the_urls):
    return f"Insert the column of the references (default '" + str(default) + "', the first column): "

