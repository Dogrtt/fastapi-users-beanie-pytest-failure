#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from db import User


@pytest.mark.usefixtures('clear_database')
class TestInvalid:
    """
    Test will never run
    """

    @pytest.mark.anyio
    async def test_admin(self, admin: User):
        print(admin)
        assert True is True
