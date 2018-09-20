#!/usr/bin/python
import os
import psycopg2
import logging
from topics import *
from subscription import *


class CampaignApiRepository:
    def __init__(self, host, db, user, password):
        conn_string = f"host='{host}' dbname='{db}' user='{user}' password='{password}'"
        logging.debug(f'Connecting to {db} database')

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
            found_activity = self.fetch_filing_activity(activity.id)
            if found_activity is None:
                # Insert new Filing Activity
                cursor.execute("""INSERT INTO filing_activity (id, version, api_version, creation_date, last_update, 
                activity_type, specification_key, origin, filing_id, aid, apply_to_filing_id, publish_sequence)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                               (activity.id, activity.version, activity.api_version, activity.creation_date,
                                activity.last_update, activity.activity_type, activity.specification_key,
                                activity.origin, activity.filing_id, activity.aid, activity.apply_to_filing_id,
                                activity.publish_sequence))
            else:
                # Update existing Filing Activity
                cursor.execute("""UPDATE filing_activity SET version=%s, creation_date=%s, last_update=%s, activity_type=%s,
                                specification_key=%s, origin=%s, filing_id=%s, aid=%s, apply_to_filing_id=%s, publish_sequence=%s
                                where id=%s""",
                               (activity.version, activity.creation_date, activity.last_update,
                                activity.activity_type, activity.specification_key, activity.origin,
                                activity.filing_id, activity.aid, activity.apply_to_filing_id,
                                activity.publish_sequence, activity.id))
            self.conn.commit()
            cursor.close()
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def fetch_filing_activity(self, activity_id):
        logging.debug("Fetching Filing Activity")
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM filing_activity WHERE id=%s", (str(activity_id),))
            a = cursor.fetchone()
            self.conn.commit()
            cursor.close()
            return a if a is None else FilingActivityV101(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9],
                                                          a[10], a[11])
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def save_filing_activity_element(self, element):
        logging.debug("Saving Filing Element")
        try:
            cursor = self.conn.cursor()
            found_element = self.fetch_filing_activity_element(element.id)
            if found_element is None:
                # Insert new Filing Element
                cursor.execute("""INSERT INTO filing_activity_element (id, api_version, creation_date, activity_id, activity_type, 
                element_type, origin, origin_filing_id, agency_id, apply_to_filing_id, publish_sequence, element_index, 
                model_json, specification_key) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                               (element.id, element.api_version, element.creation_date, element.activity_id, element.activity_type,
                                element.element_type, element.origin, element.origin_filing_id, element.agency_id,
                                element.apply_to_filing_id, element.publish_sequence, element.element_index,
                                element.model_json, element.specification_key))
            else:
                # Update existing Riling Element
                cursor.execute("""UPDATE filing_activity_element SET api_version=%s, creation_date=%s, activity_id=%s,
                 activity_type=%s, specification_key=%s, origin=%s, origin_filing_id=%s, agency_id=%s, 
                 apply_to_filing_id=%s, publish_sequence=%s, element_type=%s, model_json=%s, element_index=%s
                 where id=%s""",
                               (element.api_version, element.creation_date, element.activity_id, element.activity_type,
                                element.specification_key, element.origin, element.origin_filing_id,
                                element.agency_id, element.apply_to_filing_id, element.publish_sequence,
                                element.element_type, element.model_json, element.element_index, element.id))
            self.conn.commit()
            cursor.close()
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def fetch_filing_activity_element(self, element_id):
        logging.debug("Fetching Filing Element")
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM filing_activity_element WHERE id=%s", (str(element_id),))
            a = cursor.fetchone()
            # self.conn.commit()
            cursor.close()
            return a if a is None else FilingActivityElementV101(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8],
                                                                 a[9], a[4], a[10], a[11], a[12])
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def save_sync_subscription(self, sub):
        logging.debug("Saving Sync Subscription")
        try:
            cursor = self.conn.cursor()
            cursor.execute("""INSERT INTO sync_subscription (id, version, identity_id, feed_id, name, auto_complete, status)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                           (sub.id, sub.version, sub.identity_id, sub.feed_id, sub.name, sub.auto_complete, sub.status))
            self.conn.commit()
            cursor.close()
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def commit(self):
        self.conn.commit()

    def fetch_subscription(self, subscription_id):
        logging.debug("Fetching Active Subscription")
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM sync_subscription WHERE id=%s", (subscription_id,))
            s = cursor.fetchone()
            self.conn.commit()
            cursor.close()
            return s if s is None else SyncSubscription(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def fetch_active_subscriptions(self):
        logging.debug("Fetching Active Subscriptions")
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM sync_subscription WHERE status='Active'")
            subs = cursor.fetchall()
            self.conn.commit()
            cursor.close()
            # return s if s is None else SyncSubscription(s[0], s[1], s[2], s[3], s[4], s[5], s[6], None)
            subscriptions = []
            for s in subs:
                subscriptions.append(SyncSubscription(s[0], s[1], s[2], s[3], s[4], s[5], s[6]))
            return subscriptions
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def fetch_active_subscriptions_by_name(self, name):
        logging.debug("Fetching Active Subscriptions")
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM sync_subscription WHERE status='Active' and name=%s", (name,))
            subs = cursor.fetchall()
            self.conn.commit()
            cursor.close()
            # return s if s is None else SyncSubscription(s[0], s[1], s[2], s[3], s[4], s[5], s[6], None)
            subscriptions = []
            for s in subs:
                subscriptions.append(SyncSubscription(s[0], s[1], s[2], s[3], s[4], s[5], s[6]))
            return subscriptions
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def cancel_subscription(self, subscription_id):
        logging.debug("Canceling Active Subscriptions")
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE sync_subscription SET status='canceled' WHERE id=%s", (subscription_id,))
            self.conn.commit()
            cursor.close()
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def delete_subscription(self, subscription_id):
        logging.debug("Deleting Sync Subscription")
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM sync_subscription WHERE id=%s", (subscription_id,))
            self.conn.commit()
            cursor.close()
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()
