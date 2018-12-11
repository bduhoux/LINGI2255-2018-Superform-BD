import urllib

def php(script_path):
    urlData = urllib.urlopen(script_path)
    return urlData.read()

