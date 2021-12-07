podman build ./netlifycms-oauth-github-provider/ -t netlifyoauth
podman run -p 8000:8000 --rm netlifyoauth

https://github.com/settings/applications/new
https://github.com/settings/developers

client_id=""
client_secret=""
authorization_base_url="https://github.com/login/oauth/authorize"
token_url="https://github.com/login/oauth/access_token"
scope="repo,user"

