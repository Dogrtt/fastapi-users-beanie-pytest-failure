#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv('.env')


class BaseConfig(BaseModel):
    """Base configuration"""

    # Api
    API_NAME: str
    API_VERSION: str
    API_PREFIX_PATH: str
    API_PREFIX_VERSION: str
    API_PREFIX: str | None = None
    API_OPENAPI_URL: str = 'openapi.json'
    API_DOCS_URL: str = 'docs'
    API_REDOC_URL: str = 'redoc'

    # MongoDB
    MONGO_MAX_CONNECTIONS_COUNT: int = 0
    MONGO_MIN_CONNECTIONS_COUNT: int = 0
    MONGO_URI: str | None = None
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_USER: str
    MONGO_PASSWORD: str | None
    MONGO_DB: str

    def calculate_api_prefix(self) -> None:
        """
        Concatinate parameters to get correct API_PREFIX
        """
        if self.API_PREFIX is None:
            self.API_PREFIX = f'{self.API_PREFIX_PATH}/{self.API_PREFIX_VERSION}'

    def calculate_mongo_uri(self) -> None:
        """
        Concatinate parameters to get correct MONGO_URI
        """
        if self.MONGO_URI is None:
            self.MONGO_URI = f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}" \
                             f"@{self.MONGO_HOST}:{self.MONGO_PORT}"


def config_from_envvar() -> BaseConfig:
    """Get configuration class from environment variable"""
    loaded_config: BaseConfig = BaseConfig(**os.environ)
    loaded_config.calculate_api_prefix()
    loaded_config.calculate_mongo_uri()
    return loaded_config
