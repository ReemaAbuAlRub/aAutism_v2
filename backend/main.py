from fastapi import FastAPI
from app.routers.base import api_router
from fastapi.middleware.cors import CORSMiddleware


def include_router(app: FastAPI) -> None:
    app.include_router(api_router)

def initiate_application() -> FastAPI :
    app=FastAPI(title="Autism Chatbot", version="02")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000",
        "https://frontend.ashymeadow-e605a82c.uaenorth.azurecontainerapps.io",
        "*" ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    include_router(app)
    return app

app=initiate_application()

@app.get("/")
def run():
    return {"message":"Success"}

