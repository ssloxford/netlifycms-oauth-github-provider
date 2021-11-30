from datetime import datetime, timedelta
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import json
from pydantic import BaseSettings, HttpUrl
from requests_oauthlib import OAuth2Session
from typing import Any
from uuid import UUID

# This information is obtained upon registration of a new GitHub OAuth
# application here: https://github.com/settings/applications/new
class Settings(BaseSettings):
    client_id: str
    client_secret: str
    authorization_base_url: HttpUrl
    token_url: HttpUrl
    scope: str = "repo,user"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class StateStore:
    store = []

    def add(self, tok: str):
        self.store.append((datetime.now(), tok,))

    def contains(self, tok: str) -> bool:
        to_drop = 0
        found = False
        for (ts, t) in self.store:
            if ts < datetime.now() - timedelta(minutes=10):
                to_drop += 1
                continue

            if t == tok:
                found = True
                break

        self.store = self.store[to_drop:]
        return found

store = StateStore()

@app.get("/auth")
def auth():
    github = OAuth2Session(settings.client_id, scope=settings.scope)
    authorization_url, state = github.authorization_url(settings.authorization_base_url)
    store.add(state)
    return RedirectResponse(authorization_url)

@app.get("/callback")
def callback(state: str, request: Request):
    if not store.contains(state):
        raise HTTPException(status_code=400, detail="Invalid state")

    github = OAuth2Session(settings.client_id, state=state, scope=settings.scope)
    token = github.fetch_token(settings.token_url, client_secret=settings.client_secret, authorization_response=str(request.url))
    content = json.dumps(
        {
            "token": token.get("access_token", ""),
            "provider": "github"
        })
    return templates.TemplateResponse(
        "callback.html",
        {
            "request": request,
            "post_message": f"authorization:github:success:{content}"
        })
