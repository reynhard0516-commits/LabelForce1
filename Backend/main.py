from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import auth_routes, project_routes, task_routes
from backend.database import init_db

app = FastAPI(title="LabelForce API", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
    allow_credentials=True
)

@app.on_event("startup")
async def on_start():
    await init_db()

# Register routes
app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(project_routes.router, prefix="/projects", tags=["Projects"])
app.include_router(task_routes.router, prefix="/tasks", tags=["Tasks"])

@app.get("/")
def home():
    return {"status": "LabelForce backend running"}
