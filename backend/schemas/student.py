from pydantic import BaseModel, EmailStr

class StudentCreate(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str
    school_id: str
    grade: int
    gender: str

class StudentOut(BaseModel):
    id: int
    full_name: str
    username: str
    email: EmailStr
    school_id: str
    grade: int
    gender: str
    profile_photo: str

    class Config:
        orm_mode = True
