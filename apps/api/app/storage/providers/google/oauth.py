import json
import urllib.request
import urllib.parse
from typing import Any
from urllib.parse import urlencode

from app.storage.config import storage_settings


class GoogleOAuthManager:
    """OAuth Manager handles Google Drive API OAuth 2.0 redirection, token exchange and refresh flows."""

    def __init__(self):
        self.client_id = storage_settings.google_client_id
        self.client_secret = storage_settings.google_client_secret
        self.redirect_uri = storage_settings.google_redirect_uri

    def get_authorization_url(self, state: str | None = None) -> str:
        """Construct the Google Consent screen URL requesting offline access to Google Drive."""
        if not self.client_id:
            raise ValueError("Google Client ID is not configured.")
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/userinfo.email",
            "access_type": "offline",
            "prompt": "consent",
            "include_granted_scopes": "true",
        }
        if state:
            params["state"] = state
            
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        return f"{base_url}?{urlencode(params)}"

    def exchange_code_for_tokens(self, code: str) -> dict[str, Any]:
        """Exchange the client authorization code for access and refresh tokens."""
        if not self.client_id or not self.client_secret:
            raise ValueError("Google OAuth credentials are not configured.")

        token_url = "https://oauth2.googleapis.com/token"
        payload = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }
        
        data = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(token_url, data=data, method="POST")
        
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            token_data = json.loads(res_body)
            
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        
        # Fetch the user's email associated with the token
        email = self.fetch_account_email(access_token)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "email": email,
            "raw_response": token_data
        }

    def fetch_account_email(self, access_token: str) -> str:
        """Fetch email metadata using the user info endpoint."""
        url = "https://www.googleapis.com/oauth2/v2/userinfo"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {access_token}")
        
        with urllib.request.urlopen(req) as response:
            user_info = json.loads(response.read().decode("utf-8"))
            return user_info.get("email", "")
