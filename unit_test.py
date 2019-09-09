import unittest

from final import db, app, Data

class test(unittest.TestCase):
    def test_DB(self):
        symbol = "MSFT,AMZN,AAPL,GOOGL,FB"
        self.assertEqual(symbol, "MSFT,AMZN,AAPL,GOOGL,FB")
