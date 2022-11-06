
import os
import time
from fastapi import Body, Depends, FastAPI, HTTPException, Request, Response, status

from fastapi.responses import HTMLResponse



from .core.config import settings
from .core import helper


from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
# CORS
from fastapi.middleware.cors import CORSMiddleware

from .dependencies import get_token_header
from .internal import admin
from .routers import auth, items, users
# StaticFiles
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse 

# query token (provider) 전체 쿼리에 적용할 토큰
# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# @app.get("/")
# async def main():
#     content = """
# <body>
# <form action="/files/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# </body>
#     """
#     return HTMLResponse(content=content)


# StaticFiles
app.mount("/", StaticFiles(directory="app/static/", html=True), name="static")
# Route
@app.get("/")
async def main():
    return FileResponse('./static/index.html', media_type='text/html')

