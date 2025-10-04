from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app import routes
import httpx

app = FastAPI(
    title="Mittel Discovery",
    description="""User and article searching microservice for Mittel""",
    version="1.0.0",
    contact={
        "name": "2RinMachin",
        "url": "https://github.com/2rinMachin",
    },
)

app.include_router(routes.router)

# simple internal server error handler
# @app.exception_handler(Exception)
# async def general_exception_handler(request: Request, e: Exception):
#     return JSONResponse(
#         status_code = 500,
#         content = { "error" : "Internal server error" }
#     )
