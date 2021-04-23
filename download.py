import enum
import os
import traceback
from collections import namedtuple
from requests import get
import urllib.parse, os
from src.application.view.loading import loading
# Enum for size units
from src.infrastructure.aid import default_f_to_read, proxies, keyword, get_file_to_read_label
total_files_size = {}
# to storage the repeated urls
urls = []

class SIZE_UNIT(enum.Enum):
    BYTES = 1
    KB = 2
    MB = 3
    GB = 4

def convert_unit(size_in_bytes, unit=SIZE_UNIT.KB):
    """ Convert the size from bytes to other units like KB, MB or GB"""
    if unit == SIZE_UNIT.KB:
        return size_in_bytes / 1024
    elif unit == SIZE_UNIT.MB:
        return size_in_bytes / (1024 * 1024)
    elif unit == SIZE_UNIT.GB:
        return size_in_bytes / (1024 * 1024 * 1024)
    else:
        return size_in_bytes

def get_file_size(file_name, size_type=SIZE_UNIT.KB):
    """ Get file in size in given unit like KB, MB or GB"""
    size = os.path.getsize(file_name)
    return convert_unit(size, size_type)

FileDownloadOutput = namedtuple('FileDownloadOutput',
                                ['url', 'content_type', 'path', 'status', 'raw_size', 'raw_kb_size',
                                 'formatted_kb_size'])

# def read_file_list(file_list_txt):
#     with open(file_list_txt, 'r', encoding='cp1252') as r:
#         return r.readlines()
def read_file_list(file_name):
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
def get_file_name_with_path(url, keyword):
    try:
        '''
               Finds a path in a URL starting by keyword.
               If keyword is not found, an exception is raised.
               This method cuts off HTTP GET Parameters from file name
           '''
        if "?" in url:
            end = url.index('?')
        else:
            end = len(url)
        return url[url.index(keyword):end]
    except Exception as error:
        # pass
        print('Could not download from ', url, '\nError: ',
              traceback.format_exception_only(type(error), error)[0].rstrip())

def get_request_with_proxy(request):
    if request.next is not None:
        return_request = get(request.next.url, allow_redirects=False, proxies=proxies)
        return get_request(return_request)
    else:
        return request

def get_request_without_proxy(request):
    if request.next is not None:
        return_request = get(request.next.url, allow_redirects=False)
        return get_request(return_request)
    else:
        return request
def treats_url(url):
    # input http if not contained
    if 'http:' not in url:
        if 'https:' not in url:
            url = 'https://' + url
    return url
def extract_format_from_url(url):
    path = urllib.parse.urlparse(url).path
    ext = os.path.splitext(path)[1]
    return ext
def get_request(url):
    url = treats_url(url)
    # try with proxy
    request = get_request_with_proxy(get(url, allow_redirects=False, proxies=proxies))
    # Some requests return a 503 http code, then the request must be retried without proxy
    if request.status_code != 200:
        request = get_request_without_proxy(get(url, allow_redirects=False))
    # Some requests return other content types where client is a python application
    # So we need extract type by hands
    request.headers['content-type'] = extract_format_from_url(url)
    return request
def download_file(url):
    global total_files_size
    request = get_request(url)
    path_to_file = get_file_name_with_path(url, keyword)
    try:
        folder = os.path.dirname(path_to_file)
        if not os.path.isdir(folder):
            os.makedirs(folder)
    except Exception as error:
        # pass
        print('Could not download from ', path_to_file, '\nError: ',
              traceback.format_exception_only(type(error), error)[0].rstrip())
    with open(path_to_file, 'wb') as download_file:
        download_file.write(request.content)
    raw_kb_size = get_file_size(get_file_name_with_path(url, keyword))
    return FileDownloadOutput(url, request.headers['content-type'], get_file_name_with_path(url, keyword),
                              str(request.status_code),
                              get_file_size(get_file_name_with_path(url, keyword), SIZE_UNIT.BYTES),
                              str('{:0.10f}'.format(raw_kb_size)), str('{:0.2f}'.format(raw_kb_size)))

def download_files(f_to_find):
    file_lists = read_file_list(f_to_find)
    files_count = len(file_lists)
    file_output_status = []
    for idx, line in enumerate(file_lists):
        loading(idx + 1, files_count, prefix='Progress', suffix='Completed', length=50)
        for i in range(len(line.split(';'))):
            elegible_url = line.split(';')[i].strip().rstrip()
            try:
                file_output_status.append(download_file(elegible_url))
            except:
                # if is the last item
                if i == len(line.split(';')) - 1:
                    file_output_status.append(
                        FileDownloadOutput(elegible_url, None, get_file_name_with_path(elegible_url, keyword),
                                           'error downloading file', None, None, None))
    with open('download_result.csv', 'w') as result_csv:
        for file_status in file_output_status:
            file_name_with_path = get_file_name_with_path(file_status.url, keyword)
            if file_status.raw_size is not None:
                # concatenated total size of files
                if file_status.url not in urls:
                    urls.append(file_status.url)
                    total_files_size[file_status.content_type] = file_status.raw_size if total_files_size.get(
                        file_status.content_type) is None else total_files_size[
                                                                   file_status.content_type] + file_status.raw_size
                    if total_files_size.get(file_status.content_type + 'quantity') is None:
                        total_files_size[file_status.content_type + 'quantity'] = 0
                    total_files_size[file_status.content_type + 'quantity'] = total_files_size[file_status.content_type + 'quantity'] + 1
                result_csv.write(';'.join(
                    [file_status.url, file_name_with_path, str(file_status.raw_size), str(file_status.raw_kb_size),
                     file_status.formatted_kb_size, file_status.content_type]) + '\n')
            else:
                result_csv.write(';'.join([file_status.url, file_status.status]) + '\n')
    with open('total_sizes_result.csv', 'w') as total_sizes_result:
        for key in total_files_size.keys():
            if "text/html" in key:
                print("Contém redirecionamento para HTML, analisar os arquivos html no download_result.csv e tratar")
                continue
            else:
                if 'quantity' not in key:
                    total_sizes_result.write(key + ': ' + ' ; ' + str(total_files_size[key]) + ' ; ' + '{:0.10f}'.format(convert_unit(total_files_size[key])) + ' ; ' + '{:0.2f}'.format(convert_unit(total_files_size[key])) + ';' + str(total_files_size[key + 'quantity']) + '\n')
if __name__ == '__main__':
    f_to_find = input(get_file_to_read_label())
    f_to_find = default_f_to_read if (f_to_find is None or len(f_to_find) == 0) else f_to_find
    download_files(f_to_find)
    for key in total_files_size.keys():
        if 'quantity' not in key:
            print(key + ': ' + str(total_files_size[key]) + ' : ' + '{:0.10f}'.format(
                convert_unit(total_files_size[key])) + ' : ' + '{:0.2f}'.format(
                convert_unit(total_files_size[key])) + ' quantity: ' + str(total_files_size[key + 'quantity']))