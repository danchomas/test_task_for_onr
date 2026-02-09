from fastapi import FastAPI
import uvicorn
from routers.auth_routers import router as auth_router

app = FastAPI(
    title="auth manager",
    version="0.0.1",
    docs_url="/docs",
)

app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)