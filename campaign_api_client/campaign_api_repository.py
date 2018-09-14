#!/usr/bin/python
import os
import psycopg2
import logging
from topics import *


class CampaignApiRepository:
    def __init__(self, host, db, user, password):
        conn_string = f"host='{host}' dbname='{db}' user='{user}' password='{password}'"
        logging.debug('Connecting to database')

        try:
            # get a connection, if a connect cannot be made an exception will be raised here
            self.conn = psycopg2.connect(conn_string)
            logging.debug("Connected to database!")
        except Exception as ex:
            logging.error("Error Connecting to the database: %s" % ex)

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
            logging.error("Error: %s" % ex)
            self.conn.rollback()

    def drop_schema(self):
        logging.debug("Dropping Schema")
        try:
            cursor = self.conn.cursor()
            cursor.execute("""DROP SCHEMA public CASCADE;CREATE SCHEMA public;""")
            self.conn.commit()
            cursor.close()
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def rebuild_schema(self):
        logging.debug("Rebuilding Schema")
        self.drop_schema()
        self.execute_sql_scripts()

    def save_filing_activity(self, activity):
        logging.debug("Saving Filing Activity")
        try:
            cursor = self.conn.cursor()
            cursor.execute("""INSERT INTO filing_activity (id, version, creation_date, last_update, activity_type,
            filing_specification_key, origin, origin_filing_id, apply_to_filing_id, publish_sequence)
            VALUES (%s, %s, %s, %s,%s, %s,%s, %s,%s, %s)""",
                           (activity.id, activity.version, activity.creation_date, activity.last_update,
                            activity.filing_activity_type, activity.filing_specification_key, activity.origin,
                            activity.origin_filing_id, activity.apply_to_filing_id, activity.publish_sequence))
            self.conn.commit()
            cursor.close()
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def fetch_filing_activity(self, activity_id):
        logging.debug("Fetching Filing Activity")
        try:
            cursor = self.conn.cursor()
            cursor.execute("""SELECT * FROM filing_activity WHERE id=%s""", (str(activity_id),))
            a = cursor.fetchone()
            self.conn.commit()
            cursor.close()
            return a if a is None else FilingActivityV1(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9], a[10])
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def delete_filing_activity(self, activity_id):
        logging.debug("Deleting Filing Activity")
        try:
            cursor = self.conn.cursor()
            cursor.execute("""DELETE FROM filing_activity WHERE id=%s""", (str(activity_id),))
            self.conn.commit()
            cursor.close()
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def save_filing_element(self, element):
        logging.debug("Saving Filing Element")
        try:
            cursor = self.conn.cursor()
            cursor.execute("""INSERT INTO filing_element (id, creation_date, activity_id, activity_type, element_specification, 
            origin, origin_filing_id, agency_id, apply_to_filing_id, publish_sequence, element_index, model_json, filing_specification) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                           (element.id, element.creation_date, element.activity_id, element.filing_activity_type,
                            element.element_specification, element.origin, element.origin_filing_id, element.agency_id,
                            element.apply_to_filing_id, element.publish_sequence, element.element_index,
                            element.model_json, element.filing_specification_key))
            self.conn.commit()
            cursor.close()
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def fetch_filing_element(self, element_id):
        logging.debug("Fetching Filing Element")
        try:
            cursor = self.conn.cursor()
            cursor.execute("""SELECT * FROM filing_element WHERE id=%s""", (str(element_id),))
            a = cursor.fetchone()
            self.conn.commit()
            cursor.close()
            return a if a is None else FilingElementV1(a[0], a[1], a[2], a[3], a[12], a[5], a[6], a[7], a[8], a[9], a[4], a[10], a[11])
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def delete_filing_element(self, element_id):
        logging.debug("Deleting Filing Element")
        try:
            cursor = self.conn.cursor()
            cursor.execute("""DELETE FROM filing_element WHERE id=%s""", (str(element_id),))
            self.conn.commit()
            cursor.close()
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()
