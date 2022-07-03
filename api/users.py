from typing import List
import fastapi
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from db.db_setup import get_db, async_get_db
from pydantic_schemas.course import Course
from pydantic_schemas.user import UserCreate, User
from api.utils.users import get_user, get_user_by_email, get_users, create_user
from api.utils.courses import get_user_courses

router = fastapi.APIRouter()


@router.get("/users", response_model=List[User])
async def read_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    users = get_users(db=db, skip=skip, limit=limit)
    return users


@router.post("/users", response_model=User, status_code=201)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    _user = get_user_by_email(db=db, email=user.email)
    if _user:
        HTTPException(status_code=400, detail="Already exists")
    return create_user(db, user)


@router.get("/users/{id}", response_model=User)
async def read_user(user_id: int, db: AsyncSession = Depends(async_get_db)):
    _user = await get_user(db=db, user_id=user_id)
    if _user is None:
        raise HTTPException(status_code=404, detail="Not found")
    return _user


@router.get("/users/{user_id}/courses", response_model=List[Course])
async def read_user_courses(user_id: int, db: Session = Depends(get_db)):
    courses = get_user_courses(user_id=user_id, db=db)
    return courses
