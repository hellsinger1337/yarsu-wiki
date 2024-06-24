from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import base64
app = FastAPI()

GITHUB_API_URL = "https://api.github.com"
FRONTEND_REPO = "hellsinger1337/zzzzzzzzz"
BACKEND_REPO = "hellsinger1337/yarsu-wiki"

class Commit(BaseModel):
    title: str
    description: str
    author: str
    date: str

def get_commits(repo, since):
    url = f"{GITHUB_API_URL}/repos/{repo}/commits"
    params = {
        "since": since.isoformat()
    }
    print(f"Request URL: {url}")
    print(f"Request Params: {params}")

    response = httpx.get(url, params=params)
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")

    response.raise_for_status()
    commits = response.json()
    return [
        Commit(
            title=commit["commit"]["message"].split("\n")[0],
            description="\n".join(commit["commit"]["message"].split("\n")[1:]),
            author=commit["commit"]["author"]["name"],
            date=commit["commit"]["author"]["date"]
        )
        for commit in commits
    ]