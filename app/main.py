from fastapi import FastAPI
from app import routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Mittel Discovery",
    description="""User and article searching microservice for Mittel""",
    version="1.0.0",
    contact={
        "name": "2RinMachin",
        "url": "https://github.com/2rinMachin",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

# simple internal server error handler
# @app.exception_handler(Exception)
# async def general_exception_handler(request: Request, e: Exception):
#     return JSONResponse(
#         status_code = 500,
#         content = { "error" : "Internal server error" }
#     )
