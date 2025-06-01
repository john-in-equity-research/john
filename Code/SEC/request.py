import json
import xmltodict

class Request:

    def __init__(self, url, company=None, mail=None):
        self.url = url

        if not company:
            company = "John.AI"

        if not mail:
            mail = "mika@john.ai"

        self.headers = {
            'User-Agent': f'{company} {mail}',
        }

    def get(self, key):
        return self.fetch().get(key)

    def fetch(self, as_json=True, block_xml=False):
        # Send the GET request with the proper headers


        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()  # Will raise an exception for HTTP errors

            if self.url.endswith("xml") and not block_xml:
                return self.process_XML(response.content)

            return response.json() if as_json else response # Assuming the response is in JSON format

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    @staticmethod
    def process_XML(response):
        """ """
        return xmltodict.parse(response)
