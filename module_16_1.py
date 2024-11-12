from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Главная страница
@app.get("/")
async def read_root():
    return {"message": "Главная страница"}


# Страница администратора
@app.get("/user/admin")
async def admin():
    return {"message": "Вы вошли как администратор"}


# Страница пользователя с параметром в пути
@app.get("/user/{user_id}")
async def user(user_id: int):
    return {"message": f"Вы вошли как пользователь № {user_id}"}


# Страница пользователя с данными в адресной строке
@app.get("/user")
async def user_info(username: str, age: int):
    return {"message": f"Информация о пользователе. Имя: {username}, Возраст: {age}"}
