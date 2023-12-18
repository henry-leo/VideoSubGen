import random

import requests

from .utils import retry_on_error


class Google:
    """
    google translate
    """

    def __init__(self, source_lang: str = 'auto', object_lang: str = 'zh', proxies=None) -> None:
        self.api_url = ("https://translate.google.com/translate_a/single?client=it&dt=qca&dt=t&dt=rmt&dt=bd&"
                        "dt=rms&dt=sos&dt=md&dt=gt&dt=ld&dt=ss&dt=ex&otf=2&dj=1&hl=en&ie=UTF-8&oe=UTF-8"
                        f"&sl={source_lang}&tl={object_lang}")
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "GoogleTranslate/6.29.59279 (iPhone; iOS 15.4; en; iPhone14,2)",
        }

        self.session = requests.session()
        self.proxies = proxies

    def rotate_key(self):
        pass

    @retry_on_error(max_retries=5, wait_time=random.random())
    def translate(self, text):
        # print(text)
        query = self.session.post(
            self.api_url,
            headers=self.headers,
            data=f"q={requests.utils.quote(text)}",
            timeout=3,
            proxies=self.proxies
        )
        t_text = "".join(
            [sentence.get("trans", "") for sentence in query.json()["sentences"]],
        )
        return t_text
