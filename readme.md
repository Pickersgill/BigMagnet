# Big Magnet

For when you need a really big magnet.

This is a search and retrieval tool for the GitHub REST API.

### Quickstart

Example, finding 1000 Rust repositories under the MIT license and write to `rust_repos.json` and then downloading the archives...

```
python3 searcher.py -s 1000 -l rust -i mit -o rust_repos.json -N
python3 archive_getter.py -s rust_repos.json -o archive_directory -N
```

> [!CAUTION]
> This example uses the `-N` argument to enable execution even without a auth token. This will heavily reduce possible rate limits and thus execution time. See [the authentication section](###Authentication) for help.

### Authentication

In order to send authenticated API request the environment variable `GITHUB_TOKEN` must be set to a valid Fine-grained Personal Access Token.
Information on creating one can be found [here](https://docs.github.com/en/enterprise-server@3.9/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

### Usage

For details on how to run the tool use `python3 [searcher|archive_getter].py -h`.

For information on valid GitHub search queries see [this doc page](https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories)


