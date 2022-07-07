from fastapi import FastAPI

from .routers import bitly

app = FastAPI()
app.include_router(bitly.router)

@app.get("/")
async def root():
    return {"message": "Short url application."}

