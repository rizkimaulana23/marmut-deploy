from django.db import connection
import psycopg2


def query_add(query):
  connection.cursor().execute(query)
  connection.close()

with open('code_sql.sql', 'r') as sql_file:
    sql_query = sql_file.read()

query_add(sql_query)
