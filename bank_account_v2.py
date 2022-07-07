from flask import Flask, request, jsonify
import invalid_usage
import utils_v2
import sqlite_db

app = Flask(__name__)
InvalidUsage = invalid_usage.InvalidUsage
sqlite_db.init_db()

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
	if error.status_code == 404:
		return "", 404
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

@app.post("/account")
def create_account():
	utils_v2.verify_json(request)
	name = utils_v2.verify_name(request)
	utils_v2.duplicate_account(name)
	sqlite_db.create_account(name)
	return {"response": f'Successfully created account {name}\n'}, 200

@app.get("/account/<name>")
def get_account(name):
	account = utils_v2.account_exists(name)
	ret = {"name": account[0], "balance": round(account[1], 2)}
	return ret, 200

@app.post("/account/<name>/deposit")
def deposit(name):
	name = name.lower()
	account = utils_v2.account_exists(name)
	balance = account[1]
	amount = utils_v2.get_amount(request)
	utils_v2.positive_amount(amount)
	new_balance = balance + amount
	sqlite_db.update_balance(name, new_balance)
	return {"response": f'Successfully deposited {amount} into {name}\n'}, 200

@app.post("/account/<name>/withdraw")
def withdraw(name):
	name = name.lower()
	account = utils_v2.account_exists(name)
	balance = account[1]
	amount = utils_v2.get_amount(request)
	utils_v2.can_withdraw(amount, balance)
	new_balance = balance - amount
	sqlite_db.update_balance(name, new_balance)
	return {"response": f'Successfully withdrew {amount} from {name}\n'}, 200
