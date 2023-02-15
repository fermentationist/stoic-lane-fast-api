from .db.DB import db
import time
import functools

HOST_URL = "http://localhost:8000"
CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def shorten_url(url: str):
  existing_url = get_existing_url(url)
  if (existing_url):
    return { "status": "ok", "shortenedURL": f"{HOST_URL}/{existing_url}"}
  timestamp = round(time.time() * 1000)
  uid = int_to_encoded_string(timestamp)
  add_redirect_to_db(url, timestamp)
  return { "status": "ok", "shortenedURL": f"{HOST_URL}/{uid}"}

def int_to_encoded_string(num: int):
  output = []
  base = len(CHARS)
  while num:
    num, remainder = divmod(num, base)
    output.append(CHARS[remainder])
  output.reverse()
  return "".join(output)

def encoded_string_to_int(string: str):
  multiplier = 1
  base = len(CHARS)
  def split_string_reducer(accum, char):
    nonlocal multiplier
    nonlocal base
    int_b = int(CHARS.index(char)) * multiplier
    multiplier *= base
    return accum + int_b
  split_string = [*string]
  split_string.reverse()
  output = functools.reduce(split_string_reducer, split_string, 0)
  return output
  
def add_redirect_to_db(url: str, id: str):
  insert_query = """
    INSERT INTO redirects (url, id)
    VALUES (?, ?);
  """
  values = [url, id]
  result = db.insert(insert_query, values)
  return result

def get_existing_url(url: str):
  query = "SELECT id FROM redirects WHERE url=?"
  result = db.query(query, [url])
  row = result[0] if len(result) else []
  integer_id = row[0] if len(row) else False
  return int_to_encoded_string(integer_id) if integer_id else False

def get_full_url(redirect_id: str):
  integer_id = encoded_string_to_int(redirect_id)
  query = "SELECT url FROM redirects WHERE id = ?"
  result = db.query(query, [integer_id])
  row = result[0] if len(result) else []
  full_url = row[0] if len(row) else False
  return full_url