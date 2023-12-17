import requests


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

    def translate(self, text):
        print(text)
        """r = self.session.post(
            self.api_url,
            headers=self.headers,
            data=f"q={requests.utils.quote(text)}",
        )
        if not r.ok:
            return text
        t_text = "".join(
            [sentence.get("trans", "") for sentence in r.json()["sentences"]],
        )"""
        t_text = self._retry_translate(text, proxies=self.proxies)
        # print(re.sub("\n{3,}", "\n\n", t_text))
        return t_text

    def _retry_translate(self, text, timeout=3, proxies=None):
        time = 0
        while time <= timeout:
            time += 1
            r = self.session.post(
                self.api_url,
                headers=self.headers,
                data=f"q={requests.utils.quote(text)}",
                timeout=3,
                proxies=proxies
            )
            if r.ok:
                t_text = "".join(
                    [sentence.get("trans", "") for sentence in r.json()["sentences"]],
                )
                return t_text
        return text
