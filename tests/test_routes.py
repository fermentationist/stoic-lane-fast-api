from src import main
from src.services import shorten_url
import json
from fastapi.testclient import TestClient

client = TestClient(main.app)

def test_not_found_url():
  response = client.get("/badurl1")
  assert response.status_code == 404
  response_body = response.json()
  assert response_body["error"]["name"] == "Not found"

def test_shorten_url():
  request_body = {
    "url": "https://example.com"
  }
  response = client.post("/api/shorten-url", content=json.dumps(request_body))
  assert response.status_code == 200
  response_body = response.json()
  shortened_url = response_body["shortenedURL"]
  assert len(shortened_url)
  uid = shortened_url.replace(shorten_url.HOST_URL + "/", "")
  assert 6 < len(uid) < 9

  # shorten-url endpoint returns same shortened url for the same passed url every time
  response_2 = client.post("/api/shorten-url", content=json.dumps(request_body))
  assert response_2.status_code == 200
  response_body_2 = response_2.json()
  shortened_url_2 = response_body_2["shortenedURL"]
  assert shortened_url_2 == shortened_url

def test_redirect():
  url = f"{shorten_url.HOST_URL}/api/test?test=test_value"
  response = client.get(url)
  response_body = response.json()
  test_num = response_body["randomTestNumber"]
  query_param = response_body["testQueryParam"]

  shortened_url_response = client.post("/api/shorten-url", content=json.dumps({"url": url}))
  shortened_url_response_body = shortened_url_response.json()
  shortened_url = shortened_url_response_body["shortenedURL"]

  data_response = client.get(shortened_url)
  data_response_body = data_response.json()
  redirect_test_num = data_response_body["randomTestNumber"]
  redirect_query_param = data_response_body["testQueryParam"]
  assert test_num == redirect_test_num
  assert query_param == redirect_query_param