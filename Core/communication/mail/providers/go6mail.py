import requests
from typing import List, Dict
from Core.communication.mail.base import MailApi

class Go6MailApi(MailApi):
    MAIN_URL = "https://go6gen.pythonanywhere.com/vps_url"
    DOMAIN = "default"
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = self._get_vps_url()
    
    def _get_vps_url(self) -> str:
        try:
            resp = requests.get(self.MAIN_URL, timeout=15)
            if not resp.ok:
                raise RuntimeError(f"Failed to get VPS URL: {resp.status_code}")
            
            data = resp.json()
            vps_url = data.get("vps_url")
            if not vps_url:
                raise RuntimeError("No VPS URL in response")
            
            return vps_url.rstrip('/')
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch VPS URL: {e}")
    
    def create_account(self, username: str, password: str) -> str:
        payload = {
            "api_key": self.api_key,
            "domain": self.DOMAIN,
            "username": username,
            "password": password
        }
        
        try:
            resp = requests.post(
                f"{self.base_url}/create",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
        except requests.RequestException as e:
            raise RuntimeError(f"Network error creating Go6Mail account: {e}")
        
        if resp.status_code == 201:
            data = resp.json()
            if data.get("status") == "success":
                return data["address"]
            else:
                raise RuntimeError(f"Go6Mail creation failed: {data.get('error')}")
        
        elif resp.status_code == 401:
            raise RuntimeError("Invalid Go6Mail API key")
        elif resp.status_code == 402:
            raise RuntimeError("Insufficient Go6Mail balance")
        elif resp.status_code == 409:
            raise RuntimeError("Username already taken")
        elif resp.status_code == 400:
            data = resp.json()
            raise RuntimeError(f"Go6Mail validation error: {data.get('error')}")
        else:
            raise RuntimeError(f"Go6Mail creation failed: {resp.status_code}")
    
    def fetch_inbox(self, email: str, password: str) -> List[Dict]:
        username = email.split('@')[0]
        
        try:
            resp = requests.get(
                f"{self.base_url}/complete_inbox/{username}",
                headers={"Authorization": password},
                timeout=15
            )
        except requests.RequestException as e:
            raise RuntimeError(f"Network error fetching Go6Mail inbox: {e}")
        
        if resp.status_code == 200:
            data = resp.json()
            
            if data.get("status") == "success":
                emails = data.get("emails", [])
                formatted_emails = []
                
                for email_data in emails:
                    formatted_emails.append({
                        "id": email_data.get("id"),
                        "from": email_data.get("sender"),
                        "to": email,
                        "subject": email_data.get("subject"),
                        "body": email_data.get("body", ""),
                        "html": ""
                    })
                
                return formatted_emails
            else:
                return []
        
        elif resp.status_code == 401:
            raise RuntimeError("Invalid password for Go6Mail inbox")
        elif resp.status_code == 404:
            raise RuntimeError("Go6Mail inbox not found")
        else:
            raise RuntimeError(f"Go6Mail inbox fetch failed: {resp.status_code}")
        
## // THIS IS NOT MY CODE, THIS IS MADE MY .gekkefries1 THE OWNER OF THIS MAIL SERVICE
## // THIS IS NOT MY CODE, THIS IS MADE MY .gekkefries1 THE OWNER OF THIS MAIL SERVICE
## // THIS IS NOT MY CODE, THIS IS MADE MY .gekkefries1 THE OWNER OF THIS MAIL SERVICE
## // THIS IS NOT MY CODE, THIS IS MADE MY .gekkefries1 THE OWNER OF THIS MAIL SERVICE
