import requests, sys

class ArchiveGetter:
    def __init__(self):
        pass

    def get(self, urls, dest="./archives/"):
        print(urls)
        pass

if __name__ == "__main__":
    ag = ArchiveGetter()
    url_src = sys.argv[1]
    with open(url_src) as urls:
        ag.get([l.strip() for l in urls.readlines()])
        

    
