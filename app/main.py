from fastapi import FastAPI
from datetime import datetime
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router
from app.routers.tasks import router as tasks_router
from app.routers.admin import router as admin_router

app = FastAPI(title="Task Automation Backend")
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(admin_router)

@app.get("/info")
def info():
    return {
        "version": "0.1.0",
        "status": "ok",
        "time": datetime.utcnow().isoformat()
    }