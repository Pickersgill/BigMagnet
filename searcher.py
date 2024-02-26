import requests, argparse, os, math, sys, time

class AuthException(Exception):
    def __init__(self, message):
        self.message = message

TOKEN_ENV_VARIABLE = "GITHUB_TOKEN"

class Searcher:
    def __init__(self):
        if TOKEN_ENV_VARIABLE not in os.environ:
            raise AuthException(f"No {TOKEN_ENV_VARIABLE} env. variable found. See -h for help.")
        else:
            self.token = os.environ[TOKEN_ENV_VARIABLE]

    def search(self, query="language:rust", size=100):
        """
        Search entry point for forming requests to the GitHub API.
        Query will be injected directly into the search request and must follow API guidelines.

        EXAMPLE:
        The API request:
            https://api.github.com/search/repositories?q=language:rust+license:mit+is:public
        Can be invoked by:
            search("language:rust+license:mit+is:public")
        
        Params:
            size : int, size of search, large numbers may require pagination and take longer. If the
                number of results is fewer than size, then all results are returned.
        
        """
        PAGE_SIZE = 100
        num_of_reqs = math.ceil(size / PAGE_SIZE)
        rpm_limit = 30 if self.token else 10
        sleep_time = 60/rpm_limit
    
        fetched = 0
        results = []
        
        for i in range(num_of_reqs):
            os.system("clear")
            sys.stdout.write("Searching for results...")
            sys.stdout.write(f"\nAwaiting request {i+1} of {num_of_reqs}")
            
            page_num = fetched // PAGE_SIZE + 1
            sent = time.time()
            res = self.get_search(query, page=page_num, page_size=PAGE_SIZE)
            done = time.time()
            result = res["items"][:min(100, size-fetched)]
            fetched += len(result)
            results += result

            
            sys.stdout.write("\u001b[1K \u001b[1000D")
            sys.stdout.write(f"Received request {i+1} of {num_of_reqs}, awaiting rate limit.")
            sys.stdout.flush()
            time.sleep(max(0, sleep_time - (done-sent)))

        os.system("clear")
        print(f"Search complete, {len(results)} results found")
        return results
    
        # Paginate requests, rate limit 
    
    def get_search(self, query, page=0, page_size=100):
        """
        Send request to search endpoint and return raw result.

        Params:
            query : string, query string to append to request
            page : int, page number
            page_size : int

        """
        req_str = f"https://api.github.com/search/repositories?q={query}&per_page={page_size}&page={page}"
        res = requests.get(req_str, headers={"Authorization": f"Bearer {self.token}"})
        
        res.raise_for_status() # requests builtin will raise HTTPError if one occured
        return res.json()
        


if __name__ == "__main__":
    s = Searcher()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--size", help="Number of repositories to find", type=int, default=100, required=True) 
    parser.add_argument("-f", "--force-noauth", help="Forces execution even without auth token, results in stricter rate limit control", type=bool, default=False) 
    parser.add_argument("-l", "--language", help="The language to query for.", type=str, required=True)
    parser.add_argument("-i", "--licence", help="The license type to query for.", type=str, default="mit")
    parser.add_argument("-o", "--out", help="File location for dumping request data.", type=str, default="./out.json")

    parser.epilog = "For further information, see README."
    args = parser.parse_args()

    results = s.search(query="language:rust+license:mit+is:public", size=0)
    print(args)
    
