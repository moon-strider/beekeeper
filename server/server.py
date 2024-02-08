import os
import uvicorn
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from logging.config import dictConfig
from logging_config import log_config


dictConfig(log_config)


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

logging.info(f"connecting to mongo by url: {MONGO_URL}")


db_access = AsyncIOMotorClient(MONGO_URL)
db = db_access["db"]


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)