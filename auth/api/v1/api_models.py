from pydantic import BaseModel, validator
from spectree import SpecTree


class Signup(BaseModel):
    email: str
    password: str


class RolesPost(BaseModel):
    name: str

    @validator("name")
    def name_min_length(cls, value):
        if len(value) < 1:
            raise ValueError("Название роли не может быть пустым")
        return value


spectree = SpecTree("flask")
