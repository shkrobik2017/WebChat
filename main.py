from fastapi import FastAPI
from fastapi.routing import APIRouter

from db.db_setup import DB
from routers.chat_router.router import router as chat_router
from routers.user_router.router import router as user_router
from routers.main_page_router.router import router as main_page_router

app: FastAPI = FastAPI()

app.include_router(router=chat_router, tags=["Chat Router"])
app.include_router(router=user_router, tags=["User Router"])
app.include_router(router=main_page_router, tags=["Main Page"])


@app.on_event("startup")
async def startup() -> None:
    await DB.init_orm()


@app.on_event("shutdown")
async def shutdown() -> None:
    await DB.close_orm()
