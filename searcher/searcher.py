import requests, sys, argparse, os

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

    def search(self, size=100, **kwargs):
        """
        Search entry point for forming requests to the GitHub API.
        Via kwargs a conjunctive only version of the GitHub search syntax can be used.
        Kwargs will be injected directly into the search query.

        EXAMPLE:
        The API request:
            https://api.github.com/search/repositories?q=language:rust+license:mit+is:public
        Can be invoked by:
            search(language="rust", license="mit", is="public")
        
        Params:
            size : int, size of search, large numbers may require pagination and take longer. If the
                number of results is fewer than size, then all results are returned.
        
        """

        pass 


if __name__ == "__main__":
    s = Searcher()
    s.search(test="two")



