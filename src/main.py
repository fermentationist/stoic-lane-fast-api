from fastapi import FastAPI
from fastapi.responses import RedirectResponse
# import services.shorten_url as shorten_url_service
from .services import shorten_url as shorten_url_service
from pydantic import BaseModel

app = FastAPI()


class ShortenURLRequest(BaseModel):
  url: str


@app.post("/api/shorten-url")
async def shorten(request: ShortenURLRequest):
  print("body:", request)
  return shorten_url_service.shorten_url(request.url)


@app.get("/{redirect_id}")
async def redirect(redirect_id: str):
  result = shorten_url_service.get_full_url(redirect_id)
  if (result):
    return RedirectResponse(url=result)
  else:
    return {
      "status": "failed", 
      "status_code": 404, 
      "error": {
      "name": "Not found", 
      "message": "The requested URL was not found."
      }
    }


@app.get("/")
async def root():
  return {"answer": 42}
