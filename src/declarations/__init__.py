import json
from pathlib import Path


class Declaration:
    PATH = "declarations/{}_declaration.json"
    
    @classmethod
    def create(cls, resource_type: str, resource_data: dict):
        path = Path(cls.PATH.format(resource_type)).absolute()
        declarations = cls.read()
        if resource_data["id"] in [resource["id"] for resource in declarations]:
            raise ValueError(f"{resource_type} with id {resource_data['id']} already exists")
        declarations.append(resource_data)
        with open(path, "w") as f:
            json.dump(declarations, f, indent=4)

    @classmethod
    def read(cls, resource_type: str, resource_id=None):
        path = Path(cls.PATH.format(resource_type)).absolute()
        with open(path, "r") as f:
            declarations = json.load(f)
        if resource_id:
            return [resource for resource in declarations if resource["id"] == resource_id][0]
        return declarations

    @classmethod
    def update(cls, resource_type: str, resource_data: dict):
        path = Path(cls.PATH.format(resource_type)).absolute()
        declarations = cls.read(resource_type)
        for i, resource in enumerate(declarations):
            if resource["id"] == resource_data["id"]:
                declarations[i] = resource_data
                with open(path, "w") as f:
                    json.dump(declarations, f, indent=4)
                return
        raise ValueError(f"{resource_type} with id {resource_data['id']} does not exist")

    @classmethod
    def delete(cls, resource_type: str, resource_id):
        path = Path(cls.PATH.format(resource_type)).absolute()
        declarations = cls.read(resource_type)
        for i, resource in enumerate(declarations):
            if resource["id"] == resource_id:
                del declarations[i]
                with open(path, "w") as f:
                    json.dump(declarations, f, indent=4)
                return
        raise ValueError(f"{resource_type} with id {resource_id} does not exist")
