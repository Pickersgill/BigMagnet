import requests, sys, os, re, json
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, Pool

class PathError(Exception):
    def __init__(self, message):
        self.message = f"Path {message} does not exist."

class ArchiveGetter:
    def __init__(self, token):
        self.token = token

    def get(self, repos, dest="./archives"):
        if not os.path.exists(dest):
            raise PathError(dest)
        jobs = repos[:]
        P = 5

        while jobs:
            batch = jobs[:P]
            jobs = jobs[P:]
            pool = Pool(processes=P)
            job_params = [(owner, repo, dest) for owner, repo in batch]
            res = pool.starmap(self.fetch_archive, job_params)
    
    def fetch_archive(self, owner, repo, dest):
        print(f"Fetching {owner}/{repo}")
        req_url = f"https://api.github.com/repos/{owner}/{repo}/tarball"
        headers = {"Authorization": f"Bearer {self.token}"}
        res = requests.get(req_url, headers=headers, stream=True)
        try:
            res.raise_for_status()
            with open(f"{dest}/{owner}.{repo}.tar.gz", "wb") as file_to_write:
                for block in res.iter_content(1024):
                    file_to_write.write(block)

        except requests.exceptions.HTTPError as e:
            print(e)

if __name__ == "__main__":
    token = os.environ["GITHUB_TOKEN"]
    ag = ArchiveGetter(token)
    url_src = sys.argv[1]
    with open(url_src) as raw:
        data = json.loads(raw.read())
        repos = [(d["owner"]["login"], d["name"]) for d in data]
            
    ag.get(repos)
        

    
