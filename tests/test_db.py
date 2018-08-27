import unittest
from db.db_util import PostgresDbUtil
import json


class TestCreateDB(unittest.TestCase):

    def test_connect_db(self):
        """Rebuild campaign-api-sync database schema. This will drop existing tables during rebuild."""

        with open('../resources/config.json', 'r') as f:
            config = json.load(f)

        db_host = config['TEST']['HOST']
        db_name = config['TEST']['DB_NAME']
        db_user = config['TEST']['DB_USER']
        db_password = config['TEST']['DB_PASSWORD']
        postgres_util = PostgresDbUtil(db_host, db_name, db_user, db_password)
        postgres_util.rebuild_schema()


if __name__ == '__main__':
    unittest.main()
