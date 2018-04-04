import unittest
from fxa.config.db import db_connect


class TestDatabase(unittest.TestCase):

    def test_connection(self):
        conn, meta = db_connect()
        self.assertIsNotNone(conn)
        self.assertIsNotNone(meta)
