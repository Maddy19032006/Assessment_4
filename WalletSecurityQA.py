import unittest
from DigitalWallet import DigitalWallet


class WalletSecurityQA(unittest.TestCase):

    def setUp(self):
        self.wallet = DigitalWallet()

        self.wallet.create_account(
            "A001",
            "Maddy",
            "1234",
            20000
        )

        self.wallet.create_account(
            "A002",
            "User2",
            "5678",
            5000
        )

    # 1. Normal Transaction
    def test_normal_transaction(self):
        result = self.wallet.withdraw("A001", 1000)

        self.assertTrue(result)
        self.assertEqual(
            self.wallet.get_balance("A001"),
            19000
        )

    # 2. Insufficient Balance
    def test_insufficient_balance(self):
        result = self.wallet.withdraw("A002", 10000)

        self.assertFalse(result)
        self.assertEqual(
            self.wallet.get_balance("A002"),
            5000
        )

    # 3. Daily Limit
    def test_daily_limit(self):
        result = self.wallet.withdraw("A001", 11000)

        self.assertTrue(result)

        # Large transaction should be flagged
        self.assertTrue(
            self.wallet.is_suspicious("A001", 11000)
        )

    # 4. Multiple Failed PINs
    def test_multiple_failed_pins(self):

        self.wallet.verify_pin("A001", "1111")
        self.wallet.verify_pin("A001", "2222")
        self.wallet.verify_pin("A001", "3333")

        result = self.wallet.is_suspicious(
            "A001",
            500
        )

        self.assertTrue(result)

    # 5. Suspicious Transaction
    def test_suspicious_transaction(self):

        result = self.wallet.is_suspicious(
            "A001",
            15000
        )

        self.assertTrue(result)

    # 6. Duplicate Transaction
    def test_duplicate_transaction(self):

        self.wallet.withdraw("A001", 500)
        self.wallet.withdraw("A001", 500)

        history = self.wallet.get_transaction_history(
            "A001"
        )

        self.assertEqual(len(history), 2)

    # 7. Negative Amount
    def test_negative_amount(self):

        result = self.wallet.withdraw(
            "A001",
            -500
        )

        self.assertFalse(result)

    # 8. Concurrent Transactions
    def test_concurrent_transactions(self):

        result1 = self.wallet.withdraw(
            "A001",
            1000
        )

        result2 = self.wallet.withdraw(
            "A001",
            2000
        )

        self.assertTrue(result1)
        self.assertTrue(result2)

        self.assertEqual(
            self.wallet.get_balance("A001"),
            17000
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
