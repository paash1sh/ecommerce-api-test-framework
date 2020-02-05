import requests
import json
import os


class APIClient:

    def __init__(self):
        self.base_url = os.getenv("BASE_URL", "http://ecommerce.rivia.internal")
        self.session = requests.Session()
        self.token = None

    def authenticate(self, email, password):
        response = self.session.post(
            f"{self.base_url}/api/auth/login",
            json={"email": email, "password": password}
        )
        if response.status_code == 200:
            self.token = response.json().get("token")
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            })
        else:
            raise Exception(f"Authentication failed: {response.status_code}")

    def get(self, endpoint, params=None):
        return self.session.get(f"{self.base_url}{endpoint}", params=params)

    def post(self, endpoint, payload):
        return self.session.post(f"{self.base_url}{endpoint}", json=payload)

    def put(self, endpoint, payload):
        return self.session.put(f"{self.base_url}{endpoint}", json=payload)

    def delete(self, endpoint):
        return self.session.delete(f"{self.base_url}{endpoint}")
# api client
