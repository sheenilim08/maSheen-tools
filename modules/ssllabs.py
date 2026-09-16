import requests

ssllabs_analyze_endpoint = "https://api.ssllabs.com/api/v2/analyze"

class SslScanner:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.result = ""

    def scanStart(self):
        query_params = {
            "host": self.endpoint,
            "all": "On",
            "startNew": "On"
        }

        return self.scanFetchResult(ssllabs_analyze_endpoint, query_params)

    def scanStatus(self):
        query_params = {
            "host": self.endpoint,
            "all": "On"
        }

        return self.scanFetchResult(ssllabs_analyze_endpoint, query_params)

    def scanFetchResult(self, url, query_params):
        headers_param = {"Content-Type": "application/json"}
        response = requests.get(url, params=query_params, headers=headers_param, timeout=10)
        try:
            print(f"URL {response.url}")
            data = response.json()

            return {
                "success": True,
                "data": data
            }
        except requests.exceptions.RequestException as err:
            msg = f"An error occurred during POST: {err}"
            print(msg, err)

            return {
                "success": False,
                "message": msg
            }