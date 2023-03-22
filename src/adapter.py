import abc
from typing import List, Dict


class Adapter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def extract_data(self, source_declaration: Dict) -> List[Dict]:
        pass


class AuthenticatedAPIAdapter(Adapter):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def extract_data(self, source_declaration: Dict) -> List[Dict]:
        # TODO: Implement API authentication and data extraction
        return []


class UnauthenticatedAPIAdapter(Adapter):
    def extract_data(self, source_declaration: Dict) -> List[Dict]:
        # TODO: Implement API data extraction
        return []


class FileAdapter(Adapter):
    def extract_data(self, source_declaration: Dict) -> List[Dict]:
        # TODO: Implement file data extraction
        return []


class FTPAdapter(FileAdapter):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    # TODO: Implement FTP-specific methods


class HTTPAdapter(FileAdapter):
    # TODO: Implement HTTP-specific methods
    pass


class LocalAdapter(FileAdapter):
    # TODO: Implement local file-specific methods
    pass
