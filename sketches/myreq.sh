curl -L \
  "https://api.github.com/search/repositories?q=language:rust+license:mit&per_page=100" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -o res.json
  #-H "Accept: application/vnd.github+json" \
  #-H "Authorization: Bearer <YOUR-TOKEN>" \
