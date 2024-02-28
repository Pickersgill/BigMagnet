import requests, sys, os, re, json, argparse
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, Pool
from searcher import AuthException

class PathError(Exception):
    def __init__(self, message):
        self.message = f"Path {message} does not exist."

class ArchiveGetter:
    def __init__(self, token):
        self.token = token

    def get(self, repos, dest="./archives", batch_size=5):
        if not os.path.exists(dest):
            raise PathError(dest)
        jobs = repos[:]
        full = len(jobs)
        fetched = 0
        
        while jobs:
            os.system("clear")
            batch = jobs[:batch_size]
            jobs = jobs[batch_size:]
            sys.stdout.write(f"Fetched {fetched} of {full}...\n")
            pool = Pool(processes=batch_size)
            job_params = [(owner, repo, dest) for owner, repo in batch]
            res = pool.starmap(self.fetch_archive, job_params)
            fetched += len(batch)

        os.system("clear")
        print(f"Job complete. Fetched {full} repos to {dest}/")
    
    def fetch_archive(self, owner, repo, dest):
        sys.stdout.write(f"Fetching {owner}/{repo}\n")
        sys.stdout.flush()
        req_url = f"https://api.github.com/repos/{owner}/{repo}/tarball"
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
        else:
            headers = None
        res = requests.get(req_url, headers=headers, stream=True)
        try:
            res.raise_for_status()
            with open(f"{dest}/{owner}.{repo}.tar.gz", "wb") as file_to_write:
                for block in res.iter_content(1024):
                    file_to_write.write(block)

        except requests.exceptions.HTTPError as e:
            print(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--source", help="source file to pull repo data from", required=True, type=str) 
    parser.add_argument("-o", "--output", help="output location for fetched archives", required=True, type=str)
    parser.add_argument("-b", "--batch-size", help="batch size for multi-processing", default=5, type=int) 
    parser.add_argument("-N", "--no-auth", help="enables execution without use of a Personal Access Token", default=False, action="store_true")
    parser.add_argument("-c", "--create", help="output directory will be created if doesn't exist", default=False, action="store_true")
    
    args = parser.parse_args()
    TOKEN_ENV_VARIABLE = "GITHUB_TOKEN"
    
    token = None
    if not args.no_auth:
        if TOKEN_ENV_VARIABLE not in os.environ:
            raise AuthException(f"No {TOKEN_ENV_VARIABLE} env. variable found. See -h for help.")
        else:
            token = os.environ[TOKEN_ENV_VARIABLE]
        
    ag = ArchiveGetter(token)

    with open(args.source) as raw:
        data = json.loads(raw.read())
        data.sort(key=lambda x : x["size"]) # Sorting by size reducing wait time between processes
        repos = [(d["owner"]["login"], d["name"]) for d in data]
    
    if args.create:
        if not os.path.exists(args.output):
            os.mkdir(args.output)

    ag.get(repos, dest=args.output, batch_size=args.batch_size)
        

    
