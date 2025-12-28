from typing import Dict, Optional, Tuple
from urllib.parse import urlparse

from Core.NexusColors.color import NexusColor

class MailVerify:
    def __init__(self,  session, logger, stats) -> None:
        self.session = session
        self.logger = logger
        self.stats = stats

    def get_verify_token(self, upn: str) -> Optional[str]:
        headers: Dict[str, str] = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,de-DE;q=0.8,de;q=0.7,en-DE;q=0.6',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        }

        try:
            response = self.session.get(
                'https://click.discord.com/ls/click',
                params={'upn': upn},
                headers=headers,
                allow_redirects=False
            )
            location = response.headers.get("Location")
            if location:
                fragment = urlparse(location).fragment
                if fragment and "token=" in fragment:
                    return fragment.split("token=")[-1]
        except Exception as e:
            pass
        return None

    def verify_token(self, ctx) -> Tuple[Optional[str], bool]:
        verify_token = self.get_verify_token(ctx.upn)
        if not verify_token:
            return None, False

        try:
            response = self.session.post(
                'https://discord.com/api/v9/auth/verify',
                json={'token': verify_token}
            )
            if 200 <= response.status_code < 300:
                token = response.json().get("token")
                self.stats.ev_tokens += 1
                self.logger.log_token(f"Succsefully verified Mail -> {NexusColor.PURPLE}", token)
                ctx.token = token
                return
            
        except Exception as e:
            print(f"Error verifying token: {e}")
            with open("error.txt", "a") as f:
                f.write(e)

        return None, False