from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from models import Users, BlacklistedToken
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from config.database import get_db
from schema.schemas import CreateUserRequest, Token, CreateUserResponse
from sqlalchemy.exc import IntegrityError


router = APIRouter(
    prefix='/api/auth',
    tags=['Authentication']
)

SECRET_KEY = "9837ye4rhufi98u7yh3jie4r98uyh3jwier9f8uyh3jweirf8uy"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='api/auth/login')

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/create_user", status_code=status.HTTP_201_CREATED, response_model=dict)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    """
    Create a new user with the provided business details.
    """
    try:
        # Check if user already exists
        user_check = db.query(Users).filter(Users.business_email == create_user_request.business_email).first()
        if user_check:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists.")

        # Create new user
        create_user_model = Users(
            business_name=create_user_request.business_name,
            business_email=create_user_request.business_email,
            hashed_password=bcrypt_context.hash(create_user_request.password),
        )

        db.add(create_user_model)
        db.commit()
        db.refresh(create_user_model)

        # Return success response
        return {
            "message": "User created successfully",
            "business_name": create_user_model.business_name,
            "business_email": create_user_model.business_email,
            "business_id": create_user_model.business_id
        }

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Database integrity error. User might already exist.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")
    finally:
        db.close()


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    """
    LOGIN ROUTE
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(user.business_email, user.business_id, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}



def authenticate_user(email: str, password: str, db: Session):
    user = db.query(Users).filter(Users.business_email == email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(email: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": email, "id": user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)], db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("id")
        if email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials")
        user = db.query(Users).filter(Users.business_email == email).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")
    

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/logout")
async def logout(
    current_user: Annotated[Users, Depends(get_current_user)],
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
):
    # Create a new BlacklistedToken
    blacklisted_token = BlacklistedToken(
        token=token,
        blacklisted_on=datetime.utcnow(),
        user_id=current_user.business_id
    )
    
    # Add to database
    db.add(blacklisted_token)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not blacklist token")

    return {"message": "Successfully logged out"}