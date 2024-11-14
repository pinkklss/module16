from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()


@app.get("/user/{user_id}")
async def get_user(user_id: Annotated[int, Path(
        title="Enter User ID",
        description="User ID должен быть целым числом, больше или равно 1 и меньше или равно 100",
        ge=1,
        le=100
)]):
    return {"user_id": user_id}


@app.get("/user/{username}/{age}")
async def get_user_details(
    username: Annotated[str, Path(
        title="Enter username",
        description="Username должен быть строкой длиной от 5 до 20 символов",
        min_length=5,
        max_length=20
    )],
    age: Annotated[int, Path(
        title="Enter age",
        description="Age должен быть целым числом, больше или равно 18 и меньше или равно 120",
        ge=18,
        le=120
    )]
):
    return {"username": username, "age": age}
