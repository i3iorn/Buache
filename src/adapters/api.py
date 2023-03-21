import requests
from src.adapters import BaseAdapter


class Api(BaseAdapter):
    def __init__(self, config: dict, base_url: str = None, headers=None):
        """
        Initialize the API object.
        :param config: Adapter config dict
        :param base_url: The base URL of the API.
        :param headers: Optional HTTP headers to include in requests.
        """
        super().__init__(self)
        self.log.trace('Instantiating {}'.format(__name__))
        self.base_url = base_url or config['base_url'] or ''
        self.headers = headers or {}
        self.config = config or {}
        self.name = self.config['name']

    def __name__(self):
        return self.config['name']

    def get(self, endpoint, params=None):
        """
        Send a GET request to the API.
        :param endpoint: The endpoint to request, relative to the base URL.
        :param params: Optional parameters to include in the request.
        :return: The response from the API.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data=None):
        """
        Send a POST request to the API.
        :param endpoint: The endpoint to request, relative to the base URL.
        :param data: Optional data to include in the request body.
        :return: The response from the API.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint, data=None):
        """
        Send a PUT request to the API.
        :param endpoint: The endpoint to request, relative to the base URL.
        :param data: Optional data to include in the request body.
        :return: The response from the API.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.put(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint):
        """
        Send a DELETE request to the API.
        :param endpoint: The endpoint to request, relative to the base URL.
        :return: The response from the API.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
