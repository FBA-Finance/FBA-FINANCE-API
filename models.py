# models.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    business_name: str
    business_email: EmailStr
    password: str

class UserModel(BaseModel):
    id: str
    business_name: str
    business_email: EmailStr
    hashed_password: str

    business_size: Optional[int] = None
    registrationNumber: Optional[str] = None
    yearFounded: Optional[int] = None

    phone: Optional[str] = None
    website: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None
    industry: Optional[str] = None
    postalcode: Optional[int] = None

    annualRevenue: Optional[int] = None
    employeeCount: Optional[int] = None
    hasOutstandingLoans: Optional[bool] = None
    approximateMonthlyRevenue: Optional[float] = None
    approximateMonthlyExpenses: Optional[float] = None
    lastYearRevenue: Optional[float] = None
    currentYearProjectedRevenue: Optional[float] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    kycStatus: Optional[str] = "Unverified"


class UserResponse(BaseModel):
    id: str
    business_name: str
    business_email: EmailStr
    business_size: Optional[int] = None
    registrationNumber: Optional[str] = None
    yearFounded: Optional[int] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None
    industry: Optional[str] = None
    postalcode: Optional[int] = None
    annualRevenue: Optional[int] = None
    employeeCount: Optional[int] = None
    hasOutstandingLoans: Optional[bool] = None
    approximateMonthlyRevenue: Optional[float] = None
    approximateMonthlyExpenses: Optional[float] = None
    lastYearRevenue: Optional[float] = None
    currentYearProjectedRevenue: Optional[float] = None
    created_at: datetime
    kycStatus: Optional[str] = "Unverified"

class ProfileUserResponse(BaseModel):
    id: str
    business_name: str
    business_email: EmailStr
    registrationNumber: Optional[str] = None
    yearFounded: Optional[int] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    industry: Optional[str] = None
    kycStatus: Optional[str] = "Unverified"

class BlacklistedTokenModel(BaseModel):
    token: str
    blacklisted_on: datetime
    user_id: str


class UserUpdateModel(BaseModel):
    business_name: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)
    website: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    country: Optional[str] = Field(None)
    address: Optional[str] = Field(None)
    industry: Optional[str] = Field(None)
    postalcode: Optional[int] = Field(None)
    annualRevenue: Optional[int] = Field(None)
    employeeCount: Optional[int] = Field(None)
    hasOutstandingLoans: Optional[bool] = Field(None)
    approximateMonthlyRevenue: Optional[float] = Field(None)
    approximateMonthlyExpenses: Optional[float] = Field(None)
    lastYearRevenue: Optional[float] = Field(None)
    currentYearProjectedRevenue: Optional[float] = Field(None)

    class Config:
        extra = 'ignore'