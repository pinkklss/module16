from fastapi import FastAPI, status, Body, HTTPException, Path
from pydantic import BaseModel
from typing import List
from typing import Annotated

app = FastAPI()

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get("/users")
def get_all_users() -> List[User]:
    return users


@app.post("/user/{username}/{age}", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(username: str = Path(..., min_length=5, max_length=20, description='Enter username'),
                age: int = Path(..., ge=18, le=120, description='Enter age')) -> User:
    user_id = (users[-1].id + 1) if users else 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user


@app.delete("/user/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def delete_user(user_id: int = Path(..., description='ID of the user to delete')) -> User:
    for index, user in enumerate(users):
        if user.id == user_id:
            deleted_user = users.pop(index)
            return deleted_user
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.put("/user/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: User) -> User:
    for index, existing_user in enumerate(users):
        if existing_user.id == user_id:
            users[index] = user
            users[index].id = user_id  
            return users[index]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
