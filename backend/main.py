from fastapi import fastapi
from apis.base import api_router


def include_router(app: FastAPI) -> None:
    app.include_router(api_router)

def initiate_application() -> FastAPI :
    app=FastAPI(title="aAutism Chatbot", version="02")
    #create_database()
    include_router(app)
    return app

app=initiate_application()

@app.get("/")
def run():
    return {"message":"Success"}

