from pydantic import BaseModel, EmailStr, field_validator

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    confirm_password: str

    # Validate password + confirm_password
    @field_validator("confirm_password")
    def passwords_match(cls, v, values):
        if "password" in values.data and v != values.data["password"]:
            raise ValueError("Passwords do not match")
        return v


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True   # ✔️ Required in Pydantic V2
