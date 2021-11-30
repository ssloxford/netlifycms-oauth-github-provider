podman build ./netlifycms-oauth-github-provider/ -t netlifyoauth
podman run -p 8000:8000 --rm netlifyoauth
