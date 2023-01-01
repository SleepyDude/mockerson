from fastapi import FastAPI

from .api import root
from .api import users
from .api import fake_data

app = FastAPI()

app.include_router(root.router)
app.include_router(users.router)
app.include_router(fake_data.router)

# @app.on_event("startup")
# async def startup_event():
#     await init_deta()

# @app.on_event("shutdown")
# async def shutdown_event():
#     await shutdown_deta()
