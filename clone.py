import getpass
import sys
import traceback
from datetime import datetime
from git import Repo
from application.view.loading import loading
from infrastructure.aid import repositories_file, get_folder_to_clone_label, default_f_to_search

def clone(username, password, destiny, leave_after):
    print(f"Starting clone at ", datetime.now().strftime("%H:%M:%S"))
    if username is None or len(username) == 0:
        username = input('Username*: ')
        if username is None or len(username) == 0:
            print('You must insert the username')
            sys.exit(-1)
    if password is None or len(password) == 0:
        password = getpass.getpass('Password*: ')
        if password is None or len(password) == 0:
            print('You must insert the password')
            sys.exit(-1)
    if destiny is None or len(destiny) == 0:
        destiny = input(get_folder_to_clone_label())
        destiny = default_f_to_search if (destiny is None or len(destiny) == 0) else destiny
    # Get the count of the repositories
    l = len(open(repositories_file, 'r', encoding='cp437').readlines())
    # Save current index
    i = 0
    # Start loading bar
    loading(0, l, prefix='Progress:', suffix='Complete', length=50)
    # Read file
    with open(repositories_file, 'r', encoding='cp437') as r:
        for line in r.readlines():
            try:
                repository = line.rstrip().split(';')[0]
                project_name = repository[repository.rindex('/') + 1:len(repository)].replace('.git', '')
                branch = line.rstrip().split(';')[1]
                treated_repository = get_treated_repository(repository, username, password)
                try:
                    try_clone(repository, treated_repository, destiny, project_name, branch)
                except:
                    try:
                        try_clone(repository, treated_repository, destiny, project_name, 'ambiente-test')
                    except:
                        try:
                            try_clone(repository, treated_repository, destiny, project_name, 'develop')
                        except:
                            try:
                                try_clone(repository, treated_repository, destiny, project_name, 'release-candidate')
                            except:
                                try:
                                    try_clone(repository, treated_repository, destiny, project_name, 'master')
                                except:
                                    try:
                                        Repo(".").clone(repository)
                                    except:
                                        print(f'Error to clone ' + repository)
                i = i + 1
                loading(i, l, prefix='Cloning ' + project_name + ':', suffix='Completed',
                        length=50)
            except Exception as err:
                print(traceback.format_exception_only(type(err), err)[0].rstrip())
    print(f"Ending clone on ", datetime.now().strftime("%H:%M:%S"))
    if leave_after:
        sys.exit(-1)

def try_clone(repository, treated_repository, destiny, project_name, branch):
    Repo.clone_from(
        treated_repository,
        destiny + '/' + project_name,
        branch=branch
    )
    print(f'Cloned {project_name} from {repository} with branch {branch} ✓')

def get_treated_repository(repository, username, password):
    if 'http://' in repository:
        treated_repository = repository.replace('http://', 'http://%s:%s@')
    else:
        treated_repository = repository.replace('https://', 'https://%s:%s@')
    return treated_repository % (username, password)

if __name__ == '__main__':
    clone('', '', '', True)