from spectree import SpecTree
from pydantic import BaseModel, validator


class AuthSignup(BaseModel):
    email: str
    password: str


class RolesPost(BaseModel):
    name: str

    @validator('name')
    def name_min_length(cls, v):
        if len(v) < 1:
            raise ValueError('Название роли не может быть пустым')
        return v


spectree = SpecTree("flask")
