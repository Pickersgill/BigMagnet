curl -L \
  "https://api.github.com/search/repositories?q=language:rust+license:mit+is:public&per_page=100" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -H "Authorization: Bearer "$GITHUB_TOKEN  \
  -o ../results/test_res.json
  #-H "Accept: application/vnd.github+json" \
