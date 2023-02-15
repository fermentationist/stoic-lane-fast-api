# stoic-lane-fast-api
A URL shortener built in Python, using FastAPI. Made by [Dennis Hodges](https://dennis-hodges.com).

## Install
* `cd` into project root
* Type `python -m pip install`

## Run
* To start server, run `uvicorn src.main:app`, from project root. 
* In development, you can add the `--reload` flag for hot reloading. 
* The API is available at [localhost:8000](http://localhost:8000)

## Tests
* To run API tests, run `python -m pytest tests/` from project root.