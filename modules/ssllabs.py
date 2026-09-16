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

        self.scanFetchResult(ssllabs_analyze_endpoint, query_params)

    def scanStatus(self):
        query_params = {
            "host": self.endpoint,
            "all": "On"
        }

        self.scanFetchResult(ssllabs_analyze_endpoint, query_params)

    def scanFetchResult(self, payload):
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(ssllabs_analyze_endpoint, json=payload, headers=headers, timeout=10)
            data = response.json()

            return {
                "success": True,
                "data": data
            }
        except requests.exceptions.RequestException as err:
            msg = f"An error occurred during GET: {err}"
            print(msg)

            return {
                "success": False,
                "message": msg
            }