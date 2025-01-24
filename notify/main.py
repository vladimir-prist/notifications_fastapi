from fastapi import FastAPI
from notify import routers
from notify.database import Base, engine


# При запуске приложения создаём таблицы в БД.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Notification",
    description="Сервис рассылки (email/telegram) с отложенной отправкой."
)
app.include_router(routers.router, prefix="/api")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
