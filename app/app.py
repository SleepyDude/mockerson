from fastapi import FastAPI

from .api import fake_data

app = FastAPI()

app.include_router(fake_data.router)
