from django.db import connection

def query_add(query):
  connection.cursor().execute(query)
  connection.close()

def query_result(query):
  with connection.cursor() as cursor:
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def parse(result):
    data = result[0][0]
    return data