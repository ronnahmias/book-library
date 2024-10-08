from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator
import re

class ClientBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100, description="First name must be between 1 and 100 characters")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name must be between 1 and 100 characters")
    email: EmailStr = Field(..., description="Email must be a valid email address")
    phone: str = Field(..., min_length=10, max_length=10, description="Phone number must be 10 characters")
    
    @field_validator('phone')
    def validate_phone(cls, v):
        if not re.match(r'^05[0-689]\d{7}$', v):
            raise ValueError('Phone number must be a valid Israeli mobile number')
        return v

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100, description="First name must be between 1 and 100 characters")
    last_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Last name must be between 1 and 100 characters")
    email: Optional[EmailStr] = Field(None, description="Email must be a valid email address")
    phone: Optional[str] = Field(None, min_length=10, max_length=10, description="Phone number must be 10 characters")
    
    @field_validator('phone')
    def validate_phone(cls, v):
        if v is not None and not re.match(r'^05[0-689]\d{7}$', v):
            raise ValueError('Phone number must be a valid Israeli mobile number')
        return v

class Client(ClientBase):
    id: int

    class Config:
        from_attributes = True