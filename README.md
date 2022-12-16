# fastapi-users-beanie-pytest-failure

This is a sample repo that shows current issue with programmatic user creation.


## Error stacktrace:

````
ERROR            [ 50%]
test setup failed
anyio_backend = 'asyncio', args = (), kwargs = {}, backend_name = 'asyncio'
backend_options = {}
runner = <anyio._backends._asyncio.TestRunner object at 0x00000220D0C12F50>

    def wrapper(*args, anyio_backend, **kwargs):  # type: ignore[no-untyped-def]
        backend_name, backend_options = extract_backend_and_options(anyio_backend)
        if has_backend_arg:
            kwargs["anyio_backend"] = anyio_backend
    
        with get_runner(backend_name, backend_options) as runner:
            if isasyncgenfunction(func):
>               yield from runner.run_asyncgen_fixture(func, kwargs)

venv\Lib\site-packages\anyio\pytest_plugin.py:70: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
venv\Lib\site-packages\anyio\_backends\_asyncio.py:2158: in run_asyncgen_fixture
    self._loop.run_until_complete(f)
C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\asyncio\base_events.py:653: in run_until_complete
    return future.result()
venv\Lib\site-packages\anyio\_backends\_asyncio.py:2138: in fixture_runner
    retval = await agen.asend(None)
tests\conftest.py:47: in fixture_admin
    yield await create_user(email=EmailStr('test@test.io'), password='123456', is_superuser=True)
C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\contextlib.py:222: in __aexit__
    await self.gen.athrow(typ, value, traceback)
db.py:12: in get_user_db
    yield BeanieUserDatabase(User)
C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\contextlib.py:222: in __aexit__
    await self.gen.athrow(typ, value, traceback)
users.py:39: in get_user_manager
    yield UserManager(user_db)
tests\conftest.py:33: in create_user
    user: User = await user_manager.create(UserCreate(email=email,
venv\Lib\site-packages\fastapi_users\manager.py:131: in create
    existing_user = await self.user_db.get_by_email(user_create.email)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <fastapi_users_db_beanie.BeanieUserDatabase object at 0x00000220D2C09150>
email = 'test@test.io'

    async def get_by_email(self, email: str) -> Optional[UP_BEANIE]:
        """Get a single user by email."""
        return await self.user_model.find_one(
>           self.user_model.email == email,
            collation=self.user_model.Settings.email_collation,
        )
E       AttributeError: type object 'User' has no attribute 'email'

venv\Lib\site-packages\fastapi_users_db_beanie\__init__.py:71: AttributeError
