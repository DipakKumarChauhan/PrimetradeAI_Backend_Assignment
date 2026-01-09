from fastapi import FastAPI
from app.core import database
#from app.core.database import connect_to_mongo, close_mongo_connection, db
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.tasks import router as tasks_router

app = FastAPI(
    title="Internship Backend API",
    version="1.0.0"
)


app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")

@app.on_event("startup")
def startup_event():
    database.connect_to_mongo()


@app.on_event("shutdown")
def shutdown_event():
    database.close_mongo_connection()


@app.get("/health")
def health_check():
    #Handle case where the database connection has not been established yet
    db_status = "connected" if database.db is not None else "disconnected"
    db_name = getattr(database.db, "name", None) if database.db is not None else None
    return {"status": "ok", "db_status": db_status, "db": db_name}
     