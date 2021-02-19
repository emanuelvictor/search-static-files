import os
import sys
import traceback
from datetime import datetime
from application.view.loading import loading
from domain.entity.dependency import Dependency
from infrastructure.aid import get_folder_to_search_label, get_word_to_search_label, default_f_to_search, \
    default_w_to_search


def replace_string_in_file(project_name, file_name, string_to_search):
    if '.git' in file_name:
        return False
    dependencies = []
    # Read file
    # print(file_name)
    with open(file_name, mode='rt', errors='ignore') as teste:
        if teste.encoding != 'cp1252':
            print(teste.encoding)
    try:
        with open(file_name, mode='rt', encoding='cp437') as r:
            try:
                absolute_path = os.path.abspath(r.name)
                current_line = 0
                for content in r.readlines():
                    current_line = current_line + 1
                    if string_to_search in content:
                        dependencies.append(Dependency(project_name, absolute_path, current_line, content))
                r.close()
                # Write founded
                if len(dependencies) > 0:
                    with open('results.csv', 'a', encoding='cp437', errors='replace') as f:
                        for i in range(len(dependencies)):
                            f.write(dependencies[i].__str__())
                        f.close()
            except Exception as error:
                print('File: ' + file_name + 'Error: ' + traceback.format_exception_only(type(error), error)[0].rstrip())
    except Exception as error:
        print('File: ' + file_name + 'Error: ' + traceback.format_exception_only(type(error), error)[0].rstrip())
    return len(dependencies)

def search(f_to_search, w_to_search, leave_after):
    print(f"Starting search at ", datetime.now().strftime("%H:%M:%S"))
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
        loading(0, l, prefix='Progress:', suffix='Complete', length=50)
        for current_file in matching_file_list:
            for current_project in os.listdir(f_to_search):
                if current_project in current_file:
                    replace_string_in_file(current_project, current_file, w_to_search)
            i = i + 1
            loading(i, l, prefix='Searching :', suffix='Completed', length=50)
    except Exception as err:
        print(traceback.format_exception_only(type(err), err)[0].rstrip())
        sys.exit(-1)
    print(f"Ending search on ", datetime.now().strftime("%H:%M:%S"))
    if leave_after:
        sys.exit(-1)

if __name__ == '__main__':
    search('', '', True)