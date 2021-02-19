class Dependency:
    project = ''
    file = ''
    line = ''
    content = ''
    filetype_word_list = [".pdf", ".ts", ".js", ".png", ".jpg", ".css", ".gif", ".aspx", ".xml", ".html", ".txt"]

    def __init__(self, project, file, line, content):
        self.project = project
        self.file = file
        self.line = line
        if len(content) > 800:
            self.content = 'Content of this line is too large'
        else:
            self.content = content

    # hashcode and equals
    def __eq__(self, o: object) -> bool:
        if super().__eq__(o):
            return True
        elif self.project == Dependency(o).project and self.line == Dependency(o).line:
            return True
        else:
            return False

    def __str__(self) -> str:
        for word in self.filetype_word_list:
            if word in self.content.lower():
                return (self.project + ";" + self.file + ";" + "{}".format(
                    self.line) + ";" + word + ";" + self.content).rstrip() + "\n"
            else:
                continue

        return (self.project + ";" + self.file + ";" + "{}".format(
            self.line) + ";" + "" + ";" + self.content).rstrip() + "\n"