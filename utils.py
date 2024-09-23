from functools import wraps
from fastapi import HTTPException, status
from models import Users
from sqlalchemy.inspection import inspect

def check_profile_completion(user: Users) -> float:
    required_fields = [
        'business_size', 'registrationNumber', 'yearFounded', 'phone', 'website',
        'city', 'country', 'address', 'industry', 'postalcode', 'annualRevenue',
        'employeeCount', 'hasOutstandingLoans', 'approximateMonthlyRevenue',
        'approximateMonthlyExpenses', 'lastYearRevenue', 'currentYearProjectedRevenue'
    ]
    
    mapper = inspect(user).mapper
    column_attrs = mapper.column_attrs

    filled_fields = 0
    for field in required_fields:
        value = getattr(user, field)
        column = column_attrs[field].columns[0]
        
        # Check if the value is not None and different from the default
        if value is not None and value != column.default.arg if column.default else True:
            filled_fields += 1
    
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