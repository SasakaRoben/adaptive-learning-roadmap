from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    id: int
    username: str
    email: str
    message: str