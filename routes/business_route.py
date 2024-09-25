# business_route.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from config.database import get_db
from models import UserModel
from auth import get_current_user
from utils import MongoJSONEncoder
import json
from models import UserResponse

router = APIRouter(prefix='/v1/api/business', tags=['Business'])


@router.get("/profile", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def profile(current_user: UserModel = Depends(get_current_user)):
    return UserResponse(**current_user.dict())

@router.get("/businesses/search", response_model=List[UserResponse])
async def search_businesses(query: str = Query(..., min_length=1), db=Depends(get_db)):
    businesses = await db.users.find({
        "$or": [
            {"business_name": {"$regex": query, "$options": "i"}},
            {"industry": {"$regex": query, "$options": "i"}},
            {"city": {"$regex": query, "$options": "i"}},
            {"country": {"$regex": query, "$options": "i"}}
        ]
    }).to_list(length=None)
    
    return [UserResponse(**business, id=str(business["_id"])) for business in businesses]

@router.get("/businesses/advanced-search")
async def advanced_search_businesses(
    db=Depends(get_db),
    query: Optional[str] = Query(None, min_length=1),
    industry: Optional[str] = None,
    city: Optional[str] = None,
    country: Optional[str] = None,
    min_revenue: Optional[int] = None,
    max_revenue: Optional[int] = None,
    min_employees: Optional[int] = None,
    max_employees: Optional[int] = None,
    min_year_founded: Optional[int] = None,
    max_year_founded: Optional[int] = None,
    sort_by: Optional[str] = "business_name",
    sort_order: Optional[str] = "asc"
):
    filter_query = {}
    if query:
        filter_query["$or"] = [
            {"business_name": {"$regex": query, "$options": "i"}},
            {"industry": {"$regex": query, "$options": "i"}},
            {"city": {"$regex": query, "$options": "i"}},
            {"country": {"$regex": query, "$options": "i"}}
        ]
    if industry:
        filter_query["industry"] = industry
    if city:
        filter_query["city"] = city
    if country:
        filter_query["country"] = country
    if min_revenue:
        filter_query["annualRevenue"] = {"$gte": min_revenue}
    if max_revenue:
        filter_query["annualRevenue"] = filter_query.get("annualRevenue", {}) | {"$lte": max_revenue}
    if min_employees:
        filter_query["employeeCount"] = {"$gte": min_employees}
    if max_employees:
        filter_query["employeeCount"] = filter_query.get("employeeCount", {}) | {"$lte": max_employees}
    if min_year_founded:
        filter_query["yearFounded"] = {"$gte": min_year_founded}
    if max_year_founded:
        filter_query["yearFounded"] = filter_query.get("yearFounded", {}) | {"$lte": max_year_founded}

    sort_direction = 1 if sort_order.lower() == "asc" else -1
    businesses = await db.users.find(filter_query).sort(sort_by, sort_direction).to_list(length=None)
    return businesses

@router.get("/businesses", response_model=List[UserResponse])
async def get_all_businesses(db=Depends(get_db)):
    businesses = await db.users.find().to_list(length=None)
    return [UserResponse(**business, id=str(business["_id"])) for business in businesses]


@router.get("/businesses/{business_id}", response_model=UserResponse)
async def get_business_profile(business_id: str, db=Depends(get_db)):
    business = await db.users.find_one({"_id": ObjectId(business_id)})
    if business is None:
        raise HTTPException(status_code=404, detail="Business not found")
    return UserResponse(**business, id=str(business["_id"]))

@router.put("/profile/update", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_profile(
    profile_update: UserResponse,
    current_user: UserModel = Depends(get_current_user),
    db=Depends(get_db)
):
    update_data = profile_update.dict(exclude_unset=True, exclude={"id", "business_email", "created_at"})
    await db.users.update_one({"_id": ObjectId(current_user.id)}, {"$set": update_data})
    updated_user = await db.users.find_one({"_id": ObjectId(current_user.id)})
    return UserResponse(**updated_user, id=str(updated_user["_id"]))




# from fastapi import APIRouter, status, Query
# from typing import Annotated, Optional, List
# from sqlalchemy import or_, and_, desc, asc
# from sqlalchemy.orm import Session
# from fastapi import Depends, HTTPException
# from config.database import get_db
# from auth import get_current_user
# from models import Users
# from datetime import datetime
# from schema.schemas import ProfileResponse, BusinessProfileResponse, ProfileUpdateRequest, AdvancedBusinessSearchResponse
# from utils import check_profile_completion, require_complete_profile

# router = APIRouter(
#     prefix='/v1/api/business',
#     tags=['Business']
# )

# user_dependency = Annotated[Users, Depends(get_current_user)]
# db_dependency = Annotated[Session, Depends(get_db)]

# @router.get("/profile", status_code=status.HTTP_200_OK, response_model=ProfileResponse)
# async def profile(user: user_dependency, db: db_dependency):
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
#     current_year = datetime.now().year
#     years_in_operation = current_year - user.yearFounded if user.yearFounded else None

#     return ProfileResponse(
#         business_name=user.business_name,
#         business_email=user.business_email,
#         phone=user.phone,
#         website=user.website,
#         business_size=user.business_size,
#         employeeCount=user.employeeCount,
#         annualRevenue=user.annualRevenue,
#         registrationNumber=user.registrationNumber,
#         industry=user.industry,
#         yearFounded=user.yearFounded,
#         years_in_operation=years_in_operation
#     )


# # SEARCH FUNCTIONALITY
# @router.get("/businesses/search", response_model=List[BusinessProfileResponse])
# async def search_businesses(
#     db: db_dependency,
#     query: str = Query(..., min_length=1)
# ):
#     search = f"%{query}%"
#     businesses = db.query(Users).filter(
#         or_(
#             Users.business_name.ilike(search),
#             Users.industry.ilike(search),
#             Users.city.ilike(search),
#             Users.country.ilike(search)
#         )
#     ).all()
#     return businesses


# @router.get("/businesses/advanced-search", response_model=List[AdvancedBusinessSearchResponse])
# async def advanced_search_businesses(
#     db: Session = Depends(get_db),
#     query: Optional[str] = Query(None, min_length=1, description="Search query for business name, industry, city, or country"),
#     industry: Optional[str] = Query(None, description="Filter by industry"),
#     city: Optional[str] = Query(None, description="Filter by city"),
#     country: Optional[str] = Query(None, description="Filter by country"),
#     min_revenue: Optional[int] = Query(None, ge=0, description="Minimum annual revenue"),
#     max_revenue: Optional[int] = Query(None, ge=0, description="Maximum annual revenue"),
#     min_employees: Optional[int] = Query(None, ge=0, description="Minimum number of employees"),
#     max_employees: Optional[int] = Query(None, ge=0, description="Maximum number of employees"),
#     min_year_founded: Optional[int] = Query(None, ge=1800, le=2100, description="Minimum year founded"),
#     max_year_founded: Optional[int] = Query(None, ge=1800, le=2100, description="Maximum year founded"),
#     sort_by: Optional[str] = Query("business_name", description="Field to sort by"),
#     sort_order: Optional[str] = Query("asc", description="Sort order (asc or desc)")
# ):
#     # Start with a base query
#     businesses_query = db.query(Users)

#     # Apply search filter if query is provided
#     if query:
#         search = f"%{query}%"
#         businesses_query = businesses_query.filter(
#             or_(
#                 Users.business_name.ilike(search),
#                 Users.industry.ilike(search),
#                 Users.city.ilike(search),
#                 Users.country.ilike(search)
#             )
#         )

#     # Apply additional filters
#     if industry:
#         businesses_query = businesses_query.filter(Users.industry == industry)
#     if city:
#         businesses_query = businesses_query.filter(Users.city == city)
#     if country:
#         businesses_query = businesses_query.filter(Users.country == country)
#     if min_revenue:
#         businesses_query = businesses_query.filter(Users.annualRevenue >= min_revenue)
#     if max_revenue:
#         businesses_query = businesses_query.filter(Users.annualRevenue <= max_revenue)
#     if min_employees:
#         businesses_query = businesses_query.filter(Users.employeeCount >= min_employees)
#     if max_employees:
#         businesses_query = businesses_query.filter(Users.employeeCount <= max_employees)
#     if min_year_founded:
#         businesses_query = businesses_query.filter(Users.yearFounded >= min_year_founded)
#     if max_year_founded:
#         businesses_query = businesses_query.filter(Users.yearFounded <= max_year_founded)

#     # Apply sorting here
#     if sort_by not in AdvancedBusinessSearchResponse.__fields__:
#         raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort_by}")
#     if sort_order.lower() not in ["asc", "desc"]:
#         raise HTTPException(status_code=400, detail=f"Invalid sort order: {sort_order}")

#     sort_field = getattr(Users, sort_by)
#     if sort_order.lower() == "desc":
#         businesses_query = businesses_query.order_by(desc(sort_field))
#     else:
#         businesses_query = businesses_query.order_by(asc(sort_field))

#     # Execute query and return results
#     businesses = businesses_query.all()
#     return businesses


# @router.get("/businesses", response_model=List[BusinessProfileResponse])
# async def get_all_businesses(db: db_dependency):
#     businesses = db.query(Users).all()
#     return businesses

# @router.get("/businesses/{business_id}", response_model=BusinessProfileResponse)
# async def get_business_profile(business_id: int, db: db_dependency, user: user_dependency):
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
#     business = db.query(Users).filter(Users.business_id == business_id).first()
#     if business is None:
#         raise HTTPException(status_code=404, detail="Business not found")
#     return business



# # PROFILE UPDATE AND BUSINESS INFORMATION SETUP
# @router.put("/profile/update", status_code=status.HTTP_200_OK)
# async def update_profile(
#     profile_update: ProfileUpdateRequest,
#     current_user: Users = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     update_data = profile_update.dict(exclude_unset=True)
#     for field, value in update_data.items():
#         setattr(current_user, field, value)
    
#     db.commit()
#     db.refresh(current_user)
    
#     return {"message": "Profile updated successfully"}

