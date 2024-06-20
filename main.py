from typing import List
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from fastapi import FastAPI

from src.responses import TrendItem
from src.services import get_trends, save_trends

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/trends", response_model=List[TrendItem])
def get_trends_route():
    return get_trends()


if __name__ == "__main__":
    trends = get_trends()

    if not trends:
        save_trends()

    uvicorn.run(app, host="0.0.0.0", port=8000)
