from datetime import datetime, timedelta


class DigitalWallet:

    def __init__(self):
        self.accounts = {}
        self.transactions = {}
        self.failed_pins = {}
        self.transaction_history = {}

    # Account Creation
    def create_account(self, account_id, name, pin, balance=0):
        if account_id in self.accounts:
            return False

        self.accounts[account_id] = {
            "name": name,
            "pin": pin,
            "balance": balance
        }

        self.transactions[account_id] = []
        self.failed_pins[account_id] = 0
        self.transaction_history[account_id] = []

        return True

    # PIN Verification
    def verify_pin(self, account_id, pin):
        if account_id not in self.accounts:
            return False

        if self.accounts[account_id]["pin"] == pin:
            self.failed_pins[account_id] = 0
            return True

        self.failed_pins[account_id] += 1
        return False

    # Deposit
    def deposit(self, account_id, amount):
        if account_id not in self.accounts or amount <= 0:
            return False

        self.accounts[account_id]["balance"] += amount

        self._record_transaction(account_id, "deposit", amount)

        return True

    # Withdrawal
    def withdraw(self, account_id, amount):
        if account_id not in self.accounts:
            return False

        if amount <= 0:
            return False

        if self.accounts[account_id]["balance"] < amount:
            return False

        self.accounts[account_id]["balance"] -= amount

        self._record_transaction(account_id, "withdrawal", amount)

        return True

    # Money Transfer
    def transfer(self, sender, receiver, amount):
        if sender not in self.accounts or receiver not in self.accounts:
            return False

        if amount <= 0:
            return False

        if self.accounts[sender]["balance"] < amount:
            return False

        self.accounts[sender]["balance"] -= amount
        self.accounts[receiver]["balance"] += amount

        self._record_transaction(sender, "transfer", amount)
        self._record_transaction(receiver, "transfer_received", amount)

        return True

    # Transaction History
    def get_transaction_history(self, account_id):
        if account_id not in self.accounts:
            return []

        return self.transaction_history[account_id]

    # Balance Verification
    def get_balance(self, account_id):
        if account_id not in self.accounts:
            return None

        return self.accounts[account_id]["balance"]

    # Record Transaction
    def _record_transaction(self, account_id, transaction_type, amount):
        transaction = {
            "type": transaction_type,
            "amount": amount,
            "time": datetime.now()
        }

        self.transactions[account_id].append(transaction)
        self.transaction_history[account_id].append(transaction)

    # Fraud Detection
    def is_suspicious(self, account_id, amount):

        if account_id not in self.accounts:
            return True

        suspicious = False

        # Rule 1: Large transaction
        if amount > 10000:
            suspicious = True

        # Rule 2: Unusual transaction amount
        if amount % 100 != 0:
            suspicious = True

        # Rule 3: Multiple failed PIN attempts
        if self.failed_pins[account_id] >= 3:
            suspicious = True

        # Rule 4: More than 5 transactions in 10 minutes
        current_time = datetime.now()

        recent_transactions = [
            t for t in self.transactions[account_id]
            if current_time - t["time"] <= timedelta(minutes=10)
        ]

        if len(recent_transactions) > 5:
            suspicious = True

        return suspicious
