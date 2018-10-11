#!/usr/bin/python
import os
import sys
import psycopg2
import logging
from campaign_api_client.topics import *
from campaign_api_client.subscription import *


class CampaignApiRepository:
    def __init__(self, host, db, user, password):
        conn_string = f"host='{host}' dbname='{db}' user='{user}' password='{password}'"
        logging.debug(f'Connecting to {db} database')

        try:
            # get a connection, if a connect cannot be made an exception will be raised here
            self.conn = psycopg2.connect(conn_string)
            logging.debug("Connected to database successfully")
        except psycopg2.Error as err:
            logging.error("Database Error Connecting: %s" % err)
            sys.exit()
        except Exception as ex:
            logging.error("Unexpected error connecting to the database: %s" % ex)
            sys.exit()

    def close_connection(self):
        self.conn.close()

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
        try:
            cursor = self.conn.cursor()
            cursor.execute("""DROP SCHEMA public CASCADE;CREATE SCHEMA public;""")
            self.conn.commit()
            cursor.close()
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def rebuild_schema(self):
        self.drop_schema()
        self.execute_sql_scripts()

    def save_cal_transaction(self, transaction):
        pass

    def save_filing_activity(self, activity):
        try:
            cursor = self.conn.cursor()
            found_activity = self.fetch_filing_activity(activity.filing_activity_nid)
            if found_activity is None:
                # Insert new Filing Activity
                cursor.execute("""INSERT INTO filing_activity (filing_activity_nid, api_version, creation_date, last_update, 
                activity_type, publish_sequence, filing_nid, root_filing_nid, legal_origin, legal_filing_id,
                specification_key, legal_filing_date, start_date, end_date, apply_to_filing_id, aid)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                               (activity.filing_activity_nid, activity.api_version, activity.creation_date,
                                activity.last_update, activity.activity_type,
                                activity.publish_sequence, activity.filing.filing_nid, activity.filing.root_filing_nid,
                                activity.filing.filing_meta.legal_origin, activity.filing.filing_meta.legal_filing_id,
                                activity.filing.filing_meta.specification_key, activity.filing.filing_meta.legal_filing_date,
                                activity.filing.filing_meta.start_date, activity.filing.filing_meta.end_date,
                                activity.filing.filing_meta.apply_to_legal_filing_id, activity.filing.agency_meta.aid))
            else:
                # Update existing Filing Activity
                cursor.execute("""UPDATE filing_activity SET api_version=%s, creation_date=%s, last_update=%s, 
                activity_type=%s, publish_sequence=%s, filing_nid=%s, root_filing_nid=%s, 
                legal_origin=%s, legal_filing_id=%s, specification_key=%s, legal_filing_date=%s, start_date=%s,
                end_date=%s, apply_to_filing_id=%s, aid=%s
                where filing_activity_nid=%s""",
                               (activity.api_version, activity.creation_date, activity.last_update, activity.activity_type,
                                activity.publish_sequence, activity.filing.filing_nid, activity.filing.root_filing_nid,
                                activity.filing.filing_meta.legal_origin, activity.filing.filing_meta.legal_filing_id,
                                activity.filing.filing_meta.specification_key, activity.filing.filing_meta.legal_filing_date,
                                activity.filing.filing_meta.start_date, activity.filing.filing_meta.end_date,
                                activity.filing.filing_meta.apply_to_legal_filing_id, activity.filing.agency_meta.aid,
                                activity.filing_activity_nid))
            self.conn.commit()
            cursor.close()
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def fetch_filing_activity(self, activity_nid):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM filing_activity WHERE filing_activity_nid=%s", (str(activity_nid),))
            a = cursor.fetchone()
            self.conn.commit()
            cursor.close()
            if a is not None:
                # TODO - Add the attributes assigned to None to the DB table
                filing_meta = {'legalOrigin': a[8], 'legalFilingId': a[9], 'specificationKey': a[10], 'formId': None,
                               'legalFilingDate': a[11], 'startDate': a[12], 'endDate': a[13], 'reportNumber': None,
                               'applyToLegalFilingId': a[14]}
                filer_meta = {'longId': None, 'stringId': None, 'commonName': None, 'systemizedName': None,
                              'status': None, 'phoneList': None, 'emailList': None, 'addressList': None}
                agency_meta = {'aid': a[15], 'clientDataspaceId': None, 'applicationDataspaceId': None}
                filing = {'apiVersion': a[1], 'filingNid': a[6], 'rootFilingNid': a[7],
                          'filingMeta': filing_meta, 'filerMeta': filer_meta, 'agencyMeta': agency_meta}
                return FilingActivityV101(a[0], a[1], a[2], a[3], a[4], a[5], filing)
            else:
                return None
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def save_element_activity(self, activity):
        try:
            cursor = self.conn.cursor()
            found_element = self.fetch_element_activity(activity.element_activity_nid)
            if found_element is None:
                # Insert new Element Activity
                cursor.execute("""INSERT INTO element_activity (element_activity_nid, api_version, creation_date, 
                filing_activity_nid, activity_type, publish_sequence, element_nid, root_element_nid, filing_nid, 
                root_filing_nid, specification_key, element_classification, element_type, element_index, element_model) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                               (activity.element_activity_nid, activity.api_version, activity.creation_date,
                                activity.filing_activity_nid, activity.activity_type, activity.publish_sequence,
                                activity.filing_element.element_nid, activity.filing_element.root_element_nid,
                                activity.filing_element.filing_nid, activity.filing_element.root_filing_nid,
                                activity.filing_element.specification_key, activity.filing_element.element_classification,
                                activity.filing_element.element_type, activity.filing_element.element_index,
                                activity.filing_element.element_model))
            else:
                # Update existing Element Activity
                cursor.execute("""UPDATE element_activity SET api_version=%s, creation_date=%s, filing_activity_nid=%s,
                 activity_type=%s, publish_sequence=%s, element_nid=%s, root_element_nid=%s, 
                 filing_nid=%s, root_filing_nid=%s, specification_key=%s, element_classification=%s, element_type=%s, 
                 element_index=%s, element_model=%s where element_activity_nid=%s""",
                               (activity.api_version, activity.creation_date, activity.filing_activity_nid,
                                activity.activity_type, activity.publish_sequence, activity.filing_element.element_nid,
                                activity.filing_element.root_element_nid, activity.filing_element.filing_nid,
                                activity.filing_element.root_filing_nid, activity.filing_element.specification_key,
                                activity.filing_element.element_classification, activity.filing_element.element_type,
                                activity.filing_element.element_index, activity.filing_element.element_model,
                                activity.element_activity_nid))
            self.conn.commit()
            cursor.close()
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def fetch_element_activity(self, element_activity_nid):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM element_activity WHERE element_activity_nid=%s", (str(element_activity_nid),))
            a = cursor.fetchone()
            self.conn.commit()
            cursor.close()
            if a is not None:
                filing_element = {'elementNid': a[6], 'rootElementNid': a[7], 'filingNid': a[8],
                                  'rootFilingNid': a[9], 'specificationKey': a[10], 'elementClassification': a[11],
                                  'elementType': a[12], 'elementIndex': a[13], 'elementModel': a[14]}
                return ElementActivityV101(a[0], a[1], a[2], a[3], a[4], a[5], filing_element)
            else:
                return None
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def save_sync_subscription(self, sub):
        try:
            cursor = self.conn.cursor()
            found_subscription = self.fetch_subscription(sub.id)
            if found_subscription is None:
                # Insert new subscription
                cursor.execute("""INSERT INTO sync_subscription (id, version, identity_id, feed_id, name, auto_complete, status)
                                  VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                               (sub.id, sub.version, sub.identity_id, sub.feed_id, sub.name, sub.auto_complete,
                                sub.status))
            else:
                # Update existing Riling Element
                cursor.execute("""UPDATE sync_subscription SET version=%s, identity_id=%s,
                                 feed_id=%s, name=%s, auto_complete=%s, status=%s
                                 where id=%s""", (sub.version, sub.identity_id, sub.feed_id, sub.name, sub.auto_complete, sub.status, sub.id))

            self.conn.commit()
            cursor.close()
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def fetch_subscription(self, subscription_id):
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
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE sync_subscription SET status='canceled' WHERE id=%s", (subscription_id,))
            self.conn.commit()
            cursor.close()
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()

    def delete_subscription(self, subscription_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM sync_subscription WHERE id=%s", (subscription_id,))
            self.conn.commit()
            cursor.close()
        except Exception as ex:
            logging.error(ex)
            self.conn.rollback()
