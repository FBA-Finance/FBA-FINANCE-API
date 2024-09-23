from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional

class CreateUserRequest(BaseModel):
    business_name: str
    business_email: EmailStr
    password: str

    @validator('business_name')
    def business_name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Business name must not be empty')
        return v

    @validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

class CreateUserResponse(BaseModel):
    business_name: str
    business_email: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ProfileResponse(BaseModel):
    business_name: str
    business_email: str
    phone: str | None
    website: str | None
    business_size: int | None
    employeeCount: int | None
    annualRevenue: int | None
    registrationNumber: str | None
    industry: str | None
    yearFounded: int | None
    years_in_operation: int | None

class BusinessProfileResponse(BaseModel):
    business_name: str
    business_email: str
    industry: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    website: Optional[str] = None
    employeeCount: Optional[int] = None
    yearFounded: Optional[int] = None

    class Config:
        orm_mode = True

class ProfileUpdateRequest(BaseModel):
    business_size: Optional[int] = Field(None, ge=1)
    registrationNumber: Optional[str] = None
    yearFounded: Optional[int] = Field(None, ge=1800, le=2100)
    phone: Optional[str] = None
    website: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None
    industry: Optional[str] = None
    postalcode: Optional[int] = None
    annualRevenue: Optional[int] = Field(None, ge=0)
    employeeCount: Optional[int] = Field(None, ge=1)
    hasOutstandingLoans: Optional[bool] = None
    approximateMonthlyRevenue: Optional[float] = Field(None, ge=0)
    approximateMonthlyExpenses: Optional[float] = Field(None, ge=0)
    lastYearRevenue: Optional[float] = Field(None, ge=0)
    currentYearProjectedRevenue: Optional[float] = Field(None, ge=0)



class AdvancedBusinessSearchResponse(BaseModel):
    business_id: int
    business_name: str
    business_email: str
    industry: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    business_size: Optional[int] = None
    annualRevenue: Optional[int] = None
    yearFounded: Optional[int] = None
    employeeCount: Optional[int] = None

    class Config:
        orm_mode = True
