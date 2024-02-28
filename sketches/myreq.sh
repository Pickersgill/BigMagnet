curl -L \
  "https://api.github.com/search/repositories?q=owner:pickersgill+language:python&per_page=100" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -H "Authorization: Bearer "$GITHUB_TOKEN  \
  -o "./test.json"
  #-H "Accept: application/vnd.github+json" \
