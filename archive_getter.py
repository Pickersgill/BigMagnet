import requests, sys, os, re, json, argparse
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, Pool

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
    # TODO implement option no-auth mode
    token = os.environ["GITHUB_TOKEN"]
    ag = ArchiveGetter(token)
    
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--source", help="Source file to pull repo data from", required=True, type=str) 
    parser.add_argument("-o", "--output", help="Output location for fetched archives", required=True, type=str)
    parser.add_argument("-b", "--batch-size", help="Batch size for multi-processing", default=5, type=int) 
    
    args = parser.parse_args()

    with open(args.source) as raw:
        data = json.loads(raw.read())
        # TODO filter repos over certain size?
        data.sort(key=lambda x : x["size"])
        repos = [(d["owner"]["login"], d["name"]) for d in data]
            
    ag.get(repos, dest=args.output, batch_size=args.batch_size)
        

    
