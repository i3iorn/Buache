import json
import logging
from pathlib import Path


class Declaration:
    PATH = "declarations/{}_declaration.json"
    log = logging.getLogger('src.declaration')
    
    @classmethod
    def create(cls, resource_type: str, resource_data: dict):
        path = Path(cls.PATH.format(resource_type)).absolute()
        declarations = cls.read(resource_type, resource_data["name"])
        if resource_data["name"] in [resource["name"] for resource in declarations]:
            raise ValueError(f"{resource_type} with id {resource_data['name']} already exists")
        declarations.append(resource_data)
        with open(path, "w") as f:
            json.dump(declarations, f, indent=4)

    @classmethod
    def read(cls, resource_type: str, resource_id=None):
        path = Path(cls.PATH.format(resource_type)).absolute()
        with open(path, "r") as f:
            declarations = json.load(f)
        if resource_id:
            try:
                return [resource for resource in declarations if resource['name'] == resource_id]
            except TypeError as e:
                raise ResourceWarning(f'Tried to compare {declarations} with id: {resource_id} is of wrong type.') from e
        return declarations

    @classmethod
    def update(cls, resource_type: str, resource_data: dict):
        path = Path(cls.PATH.format(resource_type)).absolute()
        declarations = cls.read(resource_type)
        for i, resource in enumerate(declarations):
            if resource["name"] == resource_data["name"]:
                declarations[i] = resource_data
                with open(path, "w") as f:
                    json.dump(declarations, f, indent=4)
                return
        raise ValueError(f"{resource_type} with id {resource_data['name']} does not exist")

    @classmethod
    def delete(cls, resource_type: str, resource_id):
        path = Path(cls.PATH.format(resource_type)).absolute()
        declarations = cls.read(resource_type)
        for i, resource in enumerate(declarations):
            if resource["name"] == resource_id:
                del declarations[i]
                with open(path, "w") as f:
                    json.dump(declarations, f, indent=4)
                return
        raise ValueError(f"{resource_type} with id {resource_id} does not exist")
