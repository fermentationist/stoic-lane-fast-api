from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from .services import shorten_url as shorten_url_service
from pydantic import BaseModel
import random

app = FastAPI()

random_int = random.randint(1, 1000)

class ShortenURLRequest(BaseModel):
  url: str


@app.post("/api/shorten-url")
async def shorten_url(request: ShortenURLRequest):
  return shorten_url_service.shorten_url(request.url)

@app.get("/api/test")
async def test_endpoint(test: str | None = None):
  return {
    "status": "ok",
    "randomTestNumber": random_int,
    "testQueryParam": test
  }

@app.get("/{redirect_id}")
async def redirect(redirect_id: str, response: JSONResponse):
  print("redirect_id:", redirect_id)
  if not redirect_id:
    return {"answer": 66}
  result = shorten_url_service.get_full_url(redirect_id)
  if (result):
    response.status_code = status.HTTP_301_MOVED_PERMANENTLY
    return RedirectResponse(url=result)
  else:
    response.status_code = status.HTTP_404_NOT_FOUND
    return {
      "status": "failed",
      "error" : {
        "name": "Not found", 
        "message": "The requested URL was not found."
      }
    }


@app.get("/")
async def root():
  print("correct route")
  return {"answer": 42}

app.mount("/", StaticFiles(directory="static"), name="static")