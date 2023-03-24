from typing import List, Dict
from .adapter import Adapter


class Source:
    def __init__(self, source_declaration: Dict, adapter: Adapter):
        self.source_declaration = source_declaration
        self.adapter = adapter

    def get_data(self) -> List[Dict]:
        return self.adapter.extract_data(self.source_declaration)
