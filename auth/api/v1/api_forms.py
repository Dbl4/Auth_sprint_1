from spectree import SpecTree
from pydantic import BaseModel


class SignupForm(BaseModel):
    email: str
    password: str


spec = SpecTree("flask")
