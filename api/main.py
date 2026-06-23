from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Text to Graph API")

app.include_router(router)