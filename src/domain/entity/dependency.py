import re
# copied from https://stackoverflow.com/questions/6038061/regular-expression-to-find-urls-within-a-string
from src.infrastructure.aid import to_string, remove_semicolon, keyword
REGEX_URL = '(http|ftp|https)(://)([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'
class Dependency:
    project = ''
    file = ''
    line = ''
    content = ''
    filetype_word_list = [".pdf", ".ts", ".js", ".png", ".jpg", ".css", ".gif", ".aspx", ".xml", ".html", ".txt"]
    urls = ''
    def __init__(self, project, file, line, content):
        self.project = remove_semicolon(to_string(project))
        self.file = remove_semicolon(to_string(file))
        self.line = remove_semicolon(to_string(line))
        if len(content) > 800:
            self.content = 'Linha com mais de 800 caracteres'
        else:
            self.content = remove_semicolon(to_string(content))
        # url handler
        self.urls = [''.join(match) for match in re.findall(REGEX_URL, content) if
                     keyword in ''.join(match)]
        for i in range(len(self.urls)):
            self.urls[i] = remove_semicolon(to_string(self.urls[i]))
    # hashcode and equals
    def __eq__(self, o: object) -> bool:
        if super().__eq__(o):
            return True
        elif self.project == Dependency(o).project and self.line == Dependency(o).line:
            return True
        else:
            return False
    def format_string(self, word):
        return to_string(self.project + ";" + self.file + ";" + "{}".format(
            self.line) + ";" + word + ";" + self.content + ';' + ','.join(self.urls)) + "\n"
    def __str__(self) -> str:
        for word in self.filetype_word_list:
            if word in self.content.lower():
                return self.format_string(word)
            else:
                continue
        return self.format_string('')