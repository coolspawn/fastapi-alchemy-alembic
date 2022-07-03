from fastapi import FastAPI
from api import users, courses, sections
from db.db_setup import engine
from db.models import user, course

user.Base.metadata.create_all(bind=engine)
course.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fast API LMS",
    description="d",
    version="0.0.1",
    contact={"name": "Andrew", "email": "coolspawn@yandex.ru"},
    license_info={"name": "MIT"},
)
app.include_router(users.router)
app.include_router(sections.router)
app.include_router(courses.router)
