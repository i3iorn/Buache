import json
from pathlib import Path


class Declaration:
    def __init__(self, resource_type: str):
        self.resource_type = resource_type
        self.declaration_file_path = Path(f"declarations/{resource_type}_declaration.json").absolute()

    def create(self, resource_data: dict):
        declarations = self.read()
        if resource_data["id"] in [resource["id"] for resource in declarations]:
            raise ValueError(f"{self.resource_type} with id {resource_data['id']} already exists")
        declarations.append(resource_data)
        with open(self.declaration_file_path, "w") as f:
            json.dump(declarations, f, indent=4)

    def read(self, resource_id=None):
        with open(self.declaration_file_path, "r") as f:
            declarations = json.load(f)
        if resource_id:
            return [resource for resource in declarations if resource["id"] == resource_id][0]
        return declarations

    def update(self, resource_data: dict):
        declarations = self.read()
        for i, resource in enumerate(declarations):
            if resource["id"] == resource_data["id"]:
                declarations[i] = resource_data
                with open(self.declaration_file_path, "w") as f:
                    json.dump(declarations, f, indent=4)
                return
        raise ValueError(f"{self.resource_type} with id {resource_data['id']} does not exist")

    def delete(self, resource_id):
        declarations = self.read()
        for i, resource in enumerate(declarations):
            if resource["id"] == resource_id:
                del declarations[i]
                with open(self.declaration_file_path, "w") as f:
                    json.dump(declarations, f, indent=4)
                return
        raise ValueError(f"{self.resource_type} with id {resource_id} does not exist")
