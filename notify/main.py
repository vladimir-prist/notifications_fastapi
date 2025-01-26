from fastapi import FastAPI
from notify import routers
from notify.database import Base, engine

app = FastAPI(
    title="Notification",
    description="Сервис рассылки (email/telegram) с отложенной отправкой."
)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(routers.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info", reload=True)
