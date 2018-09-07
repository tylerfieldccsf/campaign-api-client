#!/usr/bin/python
import os
import psycopg2
import logging


class PostgresDbUtil:
    def __init__(self, host, db, user, password):
        conn_string = f"host='{host}' dbname='{db}' user='{user}' password='{password}'"
        print(f'Connecting to database...')

        try:
            # get a connection, if a connect cannot be made an exception will be raised here
            self.conn = psycopg2.connect(conn_string)
            print("Connected!\n")
        except Exception as ex:
            print("Error Connecting to the database: %s" % ex)

    def execute_sql_scripts(self):
        try:
            cursor = self.conn.cursor()

            logging.debug("Executing SQL scripts")
            for filename in os.listdir("../resources/sql"):
                if filename.endswith(".sql"):
                    logging.debug("Executing %s", filename)
                    sql_file = open("../resources/sql/" + filename, "r")
                    sql = sql_file.read()
                    cursor.execute(sql)
                    sql_file.close()
            self.conn.commit()

        except Exception as ex:
            print("Error: %s" % ex)

    def drop_schema(self):
        logging.debug("Dropping Schema")
        cursor = self.conn.cursor()
        cursor.execute("""DROP SCHEMA public CASCADE;CREATE SCHEMA public;""")
        self.conn.commit()

    def rebuild_schema(self):
        logging.debug("Rebuilding Schema")
        self.drop_schema()
        self.execute_sql_scripts()
