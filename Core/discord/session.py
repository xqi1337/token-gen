import curl_cffi

class DiscordSessionFactory:
    def __init__(self, proxy: str | None):
        self.proxy = proxy

    def create(self):
        session = curl_cffi.Session(impersonate="chrome")

        if self.proxy:
            session.proxies = {
                "http": f"http://{self.proxy}",
                "https": f"http://{self.proxy}",
            }

        return session
