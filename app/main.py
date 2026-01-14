from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
from app.api.v1 import campaign, health
from app.db.mongo import connect_to_mongo, close_mongo_connection
from app.core.config import settings
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This triggers the DB connection and the auto-seeding
    await connect_to_mongo()
    
    print("\n--- Registered routes on startup ---")
    for route in app.router.routes:
        methods = getattr(route, "methods", None)
        path = getattr(route, "path", None)
        print(f"  {methods} {path}")
    print("------------------------------------\n")
    
    yield
    await close_mongo_connection()

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://email-campaign-manager-frontend.vercel.app/",""],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    print(f"REQ: {request.method} {request.url.path} - STATUS: {response.status_code} ({process_time:.2f}ms)")
    return response

# Registering routers
app.include_router(campaign.router, prefix="/api/v1/campaign", tags=["Campaign"])
app.include_router(health.router, prefix="/api/v1/health", tags=["Health"])

@app.get("/")
def read_root():
    return {"status": "Backend Online"}

@app.get("/debug/routes")
async def debug_routes():
    routes = []
    for route in app.router.routes:
        methods = getattr(route, "methods", None)
        path = getattr(route, "path", None)
        routes.append({"methods": list(methods) if methods else None, "path": path})
    return routes