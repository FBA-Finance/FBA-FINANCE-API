# utils.py
from functools import wraps
from fastapi import HTTPException, status
from models import UserModel

def check_profile_completion(user: UserModel) -> float:
    required_fields = [
        'business_size', 'registrationNumber', 'yearFounded', 'phone', 'website',
        'city', 'country', 'address', 'industry', 'postalcode', 'annualRevenue',
        'employeeCount', 'hasOutstandingLoans', 'approximateMonthlyRevenue',
        'approximateMonthlyExpenses', 'lastYearRevenue', 'currentYearProjectedRevenue'
    ]
    
    filled_fields = sum(1 for field in required_fields if getattr(user, field) is not None)
    completion_percentage = (filled_fields / len(required_fields)) * 100
    return completion_percentage

def require_complete_profile(min_completion_percentage: float = 100):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not authenticated")
            
            completion_percentage = check_profile_completion(current_user)
            if completion_percentage < min_completion_percentage:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Profile is only {completion_percentage:.2f}% complete. {min_completion_percentage}% completion required for this action."
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator



from bson import ObjectId
from json import JSONEncoder
from datetime import datetime

class MongoJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)