from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Annotated, List

app = FastAPI()

users: List['User'] = []

templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/', response_class=HTMLResponse)
async def read_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get('/user/{user_id}', response_class=HTMLResponse)
async def get_user(request: Request, user_id: int):
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("users.html", {"request": request, "user": user})


@app.post('/user/{username}/{age}', response_model=User)
async def add_user(
        username: Annotated[str, Path(description="Имя пользователя")],
        age: Annotated[int, Path(description="Возраст пользователя")]) -> User:
    new_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def update_user(
        user_id: Annotated[int, Path(description="ID пользователя")],
        username: Annotated[str, Path(description="Имя пользователя")],
        age: Annotated[int, Path(description="Возраст пользователя")]) -> User:
    try:
        user = next(user for user in users if user.id == user_id)
        user.username = username
        user.age = age
        return user
    except StopIteration:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete('/user/{user_id}', response_model=User)
async def delete_user(
        user_id: Annotated[int, Path(description="ID пользователя")]) -> User:
    try:
        user = next(user for user in users if user.id == user_id)
        users.remove(user)
        return user
    except StopIteration:
        raise HTTPException(status_code=404, detail="User was not found")
