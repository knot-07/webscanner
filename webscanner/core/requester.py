import requests
from requests.exceptions import RequestException

class Requester:
    def __init__(self, timeout=10, user_agent=None, proxies=None):
        self.timeout = timeout
        self.user_agent = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        self.proxies = proxies or {}
        self.session = self._create_session()

    def _create_session(self):
        """创建请求会话"""
        session = requests.Session()
        session.headers.update({"User-Agent": self.user_agent})
        return session

    def get(self, url):
        """发送GET请求并返回结果"""
        try:
            response = self.session.get(
                url,
                timeout=self.timeout,
                proxies=self.proxies,
                allow_redirects=True,
                verify=False  # 忽略SSL证书验证
            )
            return {
                "url": response.url,
                "status": response.status_code,
                "size": len(response.content),
                "success": True
            }
        except RequestException as e:
            return {
                "url": url,
                "error": str(e),
                "success": False
            }