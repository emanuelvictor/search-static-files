import os
import re
import sys
import traceback
from datetime import datetime
from src.application.view.loading import loading
from src.domain.entity.dependency import Dependency, REGEX_URL
from src.infrastructure.aid import get_folder_to_search_label, default_f_to_search, get_word_to_search_label, \
    default_w_to_search
EXTENSIONS_IGNORE = [
    'gif',
    'jpg',
    'png',
    'pdf',
    'zip',
    'db',
    'ds_store',
    'git',
    'bak',
    'lnk',
    'scc',
    '.gitignore',
    '.git'
]
def read_file_lines(file_name):
    try:
        with open(file_name, mode='rt', encoding='utf-8') as r:
            return r.readlines()
    except:
        try:
            with open(file_name, mode='rt', encoding='cp1252') as r:
                return r.readlines()
        except:
            try:
                with open(file_name, mode='rt', encoding='cp437') as r:
                    return r.readlines()
            except Exception as error:
                print('Could not read content from ', file_name, '\nError: ',
                      traceback.format_exception_only(type(error), error)[0].rstrip())
    return []

def find_references(project_name, file_name, string_to_search):
    for extension in EXTENSIONS_IGNORE:
        if file_name.lower().endswith(extension):
            return []
    dependencies = []
    file_lines = read_file_lines(file_name)
    absolute_path = os.path.abspath(file_name)
    current_line = 0
    for content in file_lines:
        current_line = current_line + 1
        if string_to_search in content:
            dependencies.append(Dependency(project_name, absolute_path, current_line, content))
    return dependencies

def write_references(result_file, references):
    for reference in references:
        result_file.write(reference.__str__())

def search(f_to_search, w_to_search, leave_after):
    if f_to_search is None or len(f_to_search) == 0:
        f_to_search = input(get_folder_to_search_label())
        f_to_search = default_f_to_search if (f_to_search is None or len(f_to_search) == 0) else f_to_search
    if w_to_search is None or len(w_to_search) == 0:
        w_to_search = input(get_word_to_search_label())
        w_to_search = default_w_to_search if (w_to_search is None or len(w_to_search) == 0) else w_to_search
    try:
        # Walks through directory structure looking for files matching patterns
        matching_file_list = \
            [os.path.join(dp, f) \
             for dp, dn, filenames in os.walk(f_to_search) \
             for f in filenames]
        if len(matching_file_list) == 0:
            print('Not found files in here')
            return False
            # Get the count of the repositories
        l = len(matching_file_list)
        # Save current index
        i = 0
        # Start loading bar
        print(f"Starting search at ", datetime.now().strftime("%H:%M:%S"))
        loading(0, l, prefix='Progress:', suffix='Complete', length=50)
        with open('results.csv', 'a', encoding='cp1252', errors='replace') as result_file:
            for current_file in matching_file_list:
                for current_project in os.listdir(f_to_search):
                    if current_project in current_file:
                        references = find_references(current_project, current_file, w_to_search)
                        write_references(result_file, references)
                    loading(i, l, prefix='Searching :', suffix='Completed', length=50)
                i = i + 1

    except Exception as err:
        print(traceback.format_exception_only(type(err), err)[0].rstrip())
        sys.exit(-1)
    print(f"Ending search on ", datetime.now().strftime("%H:%M:%S"))
    if leave_after:
        sys.exit(-1)

if __name__ == '__main__':
    search('', '', True)
    # content = '  <script src="http://www.itau.com.br/_arquivosestaticos/Itau/defaultTheme/js/metricas/pj/8c717b434098baa16315c685ff81572aae207a9b/satelliteLib-1e0f7b069fdd16b664ae10e740c413649330dffb.js"></script>   <script src="http://www.itau.com.br/_arquivosestaticos/Itau/defauf81572aa649330dffb.js"></script>'
    #
    # urls = [''.join(match) for match in re.findall(REGEX_URL, content) if '_arquivosestaticos' in ''.join(match)]
    #
    # urls = ','.join(str(url) for url in urls)
    #
    # print(urls.__str__())
    #
    # list1 = [1, 2, 3]
    # str1 = ''.join(str(e) for e in list1)
    #
    # print(str1)