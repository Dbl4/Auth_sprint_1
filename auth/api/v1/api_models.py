from spectree import SpecTree
from pydantic import BaseModel


class AuthSignup(BaseModel):
    email: str
    password: str


spectree = SpecTree("flask")
