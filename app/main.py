from fastapi import FastAPI
# import uvicorn
# import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from libs.GeminiAI import response_generator

app = FastAPI()

origins = ["https://abal-abal.vercel.app", "http://localhost", "http://localhost:5173","https://vercel.app","https://vercel.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RequestMessage(BaseModel):
    message: str
    style: str


@app.get("/")
async def root():
    return {"message": "Hello World Abal-Abal"}


@app.post("/request-message/")
async def message(
    request: RequestMessage,
):
    return StreamingResponse(
        response_generator(request.message, request.style),
        media_type="application/x-ndjson",
    )


# default_port = "8080"
# try:
#     port = int(float(os.environ.get("PORT", default_port)))
# except TypeError:
#     port = int(default_port)

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
