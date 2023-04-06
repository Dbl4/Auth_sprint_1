from spectree import SpecTree
from pydantic import BaseModel
from uuid import UUID


class SignupForm(BaseModel):
    email: str
    password: str


class RolesPost(BaseModel):
    name: str


spec = SpecTree("flask")
