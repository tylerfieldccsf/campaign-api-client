#!/usr/bin/python
import os
import psycopg2
import logging
from models import *


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
            cursor.close()

        except Exception as ex:
            print("Error: %s" % ex)
            self.conn.rollback()

    def drop_schema(self):
        logging.debug("Dropping Schema")
        try:
            cursor = self.conn.cursor()
            cursor.execute("""DROP SCHEMA public CASCADE;CREATE SCHEMA public;""")
            self.conn.commit()
            cursor.close()
        except Exception as ex:
            print(ex)
            self.conn.rollback()

    def rebuild_schema(self):
        logging.debug("Rebuilding Schema")
        self.drop_schema()
        self.execute_sql_scripts()

    def save_flare_activity(self, activity):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""INSERT INTO flare_activity (id, version, creation_date, last_update, activity_type,
            filing_specification_key, origin, origin_filing_id, apply_to_filing_id, publish_sequence)
            VALUES (%s, %s, %s, %s,%s, %s,%s, %s,%s, %s)""",
                           (str(activity.id), activity.version, activity.creation_date, activity.last_update,
                            activity.filing_activity_type.name, activity.filing_specification_key, activity.origin,
                            activity.origin_filing_id, activity.apply_to_filing_id, activity.publish_sequence))
            self.conn.commit()
            cursor.close()
        except Exception as ex:
            print(ex)
            self.conn.rollback()

    def fetch_flare_activity(self, activity_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""SELECT * FROM flare_activity WHERE id=%s""", (str(activity_id),))
            a = cursor.fetchone()
            self.conn.commit()
            cursor.close()
            return a if a is None else FlareActivity(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10])
        except Exception as ex:
            print(ex)
            self.conn.rollback()

    def delete_flare_activity(self, activity_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""DELETE FROM flare_activity WHERE id=%s""", (str(activity_id),))
            self.conn.commit()
            cursor.close()
        except Exception as ex:
            print(ex)
            self.conn.rollback()
