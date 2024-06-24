from typing import Optional

import requests
from fastapi import APIRouter, HTTPException, Query

from src.config.config import config

router = APIRouter()


def save_user_credentials(creds):
    # Implement saving credentials to the backend here
    print(creds)
    print(creds)
    print(creds)
    print(creds)
    print(creds)
    return

    backend_url = config.BACKEND_URL
    response = requests.post(backend_url, json=creds)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Failed to save user credentials"
        )


@router.get("/gauth/callback")
async def callback(
    access_token: Optional[str] = Query(None),
    token_type: Optional[str] = Query(None),
    expires_in: Optional[str] = Query(None),
    scope: Optional[str] = Query(None),
    authuser: Optional[str] = Query(None),
    prompt: Optional[str] = Query(None),
):
    if not access_token:
        raise HTTPException(status_code=400, detail="Missing access_token")

    creds = {
        "access_token": access_token,
        "token_type": token_type,
        "expires_in": expires_in,
        "scope": scope,
        "authuser": authuser,
        "prompt": prompt,
    }

    save_user_credentials(creds)
    return {"message": "User authenticated successfully", "credentials": creds}
