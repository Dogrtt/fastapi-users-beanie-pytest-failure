#!/usr/bin/env python
# -*- coding: utf-8 -*-
import contextlib

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr
from pymongo import MongoClient
from pytest import fixture

from config import BaseConfig, config_from_envvar
from db import get_user_db, User
from schemas import UserCreate
from users import get_user_manager

config: BaseConfig = config_from_envvar()
mongo_client = MongoClient(config.MONGO_URI)

get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(*, email: EmailStr,
                      password: str,
                      is_active: bool = True,
                      is_verified: bool = True,
                      is_superuser: bool = False) -> User | None:
    """
    Create new Super User
    """
    try:
        async with get_user_db_context() as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                user: User = await user_manager.create(UserCreate(email=email,
                                                                  password=password,
                                                                  is_superuser=is_superuser,
                                                                  is_active=is_active,
                                                                  is_verified=is_verified
                                                                  ))
                return user
    except UserAlreadyExists as error:
        print(f'Something is wrong: {error=}')
        return


@fixture(name='admin')
async def fixture_admin() -> User:
    yield await create_user(email=EmailStr('test@test.io'), password='123456', is_superuser=True)


@fixture
def clear_database() -> None:
    """
    Completely remove database
    """
    mongo_client.drop_database(config.MONGO_DB)
    yield
