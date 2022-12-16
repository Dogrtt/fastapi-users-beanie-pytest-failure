#!/usr/bin/env python
# -*- coding: utf-8 -*-
from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

from config import config_from_envvar
from db import User
from schemas import UserRead, UserCreate, UserUpdate
from users import fastapi_users, auth_backend

config = config_from_envvar()
app = FastAPI(title=config.API_NAME,
              version=config.API_VERSION,
              openapi_url=f'{config.API_PREFIX}/{config.API_OPENAPI_URL}',
              docs_url=f'{config.API_PREFIX}/{config.API_DOCS_URL}',
              redoc_url=f'{config.API_PREFIX}/{config.API_REDOC_URL}',
              swagger_ui_parameters={"docExpansion": "none"})

auth_api_prefix = f'{config.API_PREFIX}/auth'
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate),
                   prefix=auth_api_prefix,
                   tags=['Auth'])
app.include_router(fastapi_users.get_auth_router(auth_backend, requires_verification=True),
                   prefix=auth_api_prefix,
                   tags=['Auth'])
app.include_router(fastapi_users.get_verify_router(UserRead),
                   prefix=auth_api_prefix,
                   tags=["Auth"])
app.include_router(fastapi_users.get_reset_password_router(),
                   prefix=auth_api_prefix,
                   tags=["Auth"])
app.include_router(fastapi_users.get_users_router(UserRead,
                                                  UserUpdate,
                                                  requires_verification=True),
                   prefix=f'{config.API_PREFIX}/users',
                   tags=["Auth"])

db_client = AsyncIOMotorClient(config.MONGO_URI,
                               socketTimeoutMS=300000,
                               connectTimeoutMS=300000,
                               serverSelectionTimeoutMS=300000,
                               waitQueueTimeoutMS=300000,
                               maxPoolSize=config.MONGO_MAX_CONNECTIONS_COUNT,
                               minPoolSize=config.MONGO_MIN_CONNECTIONS_COUNT)


@app.on_event('stratup')
async def on_startup():
    await init_beanie(
        database=db_client[config.MONGO_DB],
        document_models=[
            User,
        ]
    )


@app.on_event('shutdown')
async def close_connections():
    client = MongoClient(config.MONGO_URI)
    client.drop_database(config.MONGO_DB)
