from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse, JSONResponse
# import services.shorten_url as shorten_url_service
from .services import shorten_url as shorten_url_service
from pydantic import BaseModel
import random

app = FastAPI()

random_int = random.randint(1, 1000)

class ShortenURLRequest(BaseModel):
  url: str


@app.post("/api/shorten-url")
async def shorten(request: ShortenURLRequest):
  return shorten_url_service.shorten_url(request.url)

@app.get("/api/test")
async def test_endpoint(test: str | None = None):
  print("q in controller:", test)
  return {
    "status": "ok",
    "randomTestNumber": random_int,
    "testQueryParam": test
  }

@app.get("/{redirect_id}")
async def redirect(redirect_id: str, response: JSONResponse):
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
  return {"answer": 42}
