import os
import uvicorn
import logging

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorClient
from logging.config import dictConfig
from logging_config import log_config
from datetime import timedelta
from utils.security import pwd_context, create_access_token
from models import User, TokenData
from jose import JWTError, jwt
from utils.security import JWT_ALGORITHM, JWT_SECRET_KEY


dictConfig(log_config)

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
MONGO_URL = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@database:27017/db?authSource=admin"
logging.debug(f"Connected to mongodb by url: {MONGO_URL}")


db_access = AsyncIOMotorClient(MONGO_URL)
db = db_access["db"]


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await db["users"].find_one({"username": token_data.username})
    if user is None:
        raise credentials_exception
    return token_data.username


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.get("/users")
async def get_all_users():
    users = []
    cursor = db["users"].find({}, {'_id': False})
    logging.debug(f"fetched cursor: {cursor}")
    async for user in cursor:
        users.append(user)
    logging.debug(f"fetching {users} from database...")
    return users


@app.post("/register")
async def register(user: User):
    hashed_password = pwd_context.hash(user.password)
    user_dict = user.model_dump()
    user_dict["password"] = hashed_password
    await db["users"].insert_one(user_dict)
    return {"message": "User registered successfully"}


@app.post("/login", response_model=TokenData)
async def login(form_data: User):
    user = await db["users"].find_one({"username": form_data.username})
    if not user or not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)