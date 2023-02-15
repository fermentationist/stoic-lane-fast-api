# stoic-lane-fast-api
A URL shortener built in Python, using FastAPI. Made by [Dennis Hodges](https://dennis-hodges.com).

## Install
1. `cd` into project root
2. Create virtual environment with `python -m venv .`
3. To activate virtual environment, type `source bin/activate`
4. To install dependencies, type `python -m pip install -r requirements.txt`

## Run
* To start server, run `uvicorn src.main:app`, from project root. 
* In development, you can add the `--reload` flag for hot reloading. 
* The API is available at [localhost:8000](http://localhost:8000)

## Tests
* To run API tests, run `python -m pytest tests/` from project root.