from config.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = 'users'

    business_id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String, nullable=False)
    business_email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # More Business Details
    business_size = Column(Integer, nullable=True)
    registrationNumber = Column(String, nullable=True)
    yearFounded = Column(Integer, nullable=True)
    phone = Column(String, nullable=True)
    website = Column(String, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    address = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    postalcode = Column(Integer, nullable=True)

    # Financial Information
    annualRevenue = Column(Integer, nullable=True)
    employeeCount = Column(Integer, nullable=True)
    hasOutstandingLoans = Column(Boolean, nullable=True)
    approximateMonthlyRevenue = Column(Float, nullable=True)
    approximateMonthlyExpenses = Column(Float, nullable=True)
    lastYearRevenue = Column(Float, nullable=True)
    currentYearProjectedRevenue = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    kycStatus = Column(String, nullable=True)

class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    blacklisted_on = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.business_id"))
    user = relationship("Users")