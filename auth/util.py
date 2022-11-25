import re

regex = re.compile(".+code=(?P<code>.+)&state=(?P<state>.+)")


def search_code_path(path, name):
    return re.search(regex, path).group(name)


def format_redirect_uri(port):
    return "http://localhost:{}".format(port)
