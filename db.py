#!/usr/bin/env python
# -*- coding: utf-8 -*-
from beanie import PydanticObjectId
from fastapi_users_db_beanie import BeanieBaseUser, BeanieUserDatabase


class User(BeanieBaseUser[PydanticObjectId]):
    pass


async def get_user_db():
    yield BeanieUserDatabase(User)
