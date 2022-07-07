# Utility Functions
import invalid_usage
import sqlite_db
InvalidUsage = invalid_usage.InvalidUsage

def verify_json(request):
	if not request.is_json:
		raise InvalidUsage("Request must be JSON", status_code=400)

def verify_name(request):
	params = request.get_json()
	if "name" not in params:
		raise InvalidUsage("name of account must be given", status_code=400)
	name = params['name'].strip().lower()
	return name

def duplicate_account(name):
	account = sqlite_db.get_account(name)
	if account:
		raise InvalidUsage("Account name already exists", status_code=400)

def account_exists(name):
	account = sqlite_db.get_account(name)
	if not account:
		raise InvalidUsage("", status_code=404)
	return account

def get_amount(request):
	params = request.get_json()
	if "amount" not in params:
		raise InvalidUsage("amount must be given", status_code=400)
	return params['amount']

def positive_amount(amount):
	if amount <= 0:
		raise InvalidUsage("amount must be greater than 0", status_code=400)

def can_withdraw(amount, balance):
	if amount > balance:
		raise InvalidUsage("amount must be less than the account balance", status_code=400)