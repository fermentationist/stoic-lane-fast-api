import sqlite3
from .init_tables import init

class DB():
  def __init__(self, db, filename):
    self.db = db
    self.connection = db.connect(filename, check_same_thread=False)
    print("DB initialized")
    self.query(init)

  def query(self, query_string, values=[]):
    cursor = self.connection.cursor()
    try:
      result = cursor.execute(query_string, values)
      return result.fetchall()
    except self.db.Error as error:
      print("DB query error:", error)
      raise Exception(error) 
    finally:
      cursor.close()

  def insert(self, query_string, values=[]):
    cursor = self.connection.cursor()
    try:
      result = cursor.execute(query_string, values)
      self.connection.commit()
      return result.fetchall()
    except self.db.Error as error:
      print("DB insert error:", error)
      raise Exception(error) 
    finally:
      cursor.close()

db = DB(sqlite3, "src/services/db/database.db")
