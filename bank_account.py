from flask import Flask, request, jsonify
import invalid_usage
import utils

app = Flask(__name__)
InvalidUsage = invalid_usage.InvalidUsage
accounts = {}

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
	if error.status_code == 404:
		return "", 404
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

@app.post("/account")
def create_account():
	utils.verify_json(request)
	name = utils.verify_name(request)
	utils.duplicate_account(accounts, name)
	accounts[name] = 0.00
	return {"response": f'Successfully created account {name}\n'}, 200

@app.get("/account/<name>")
def get_account(name):
	utils.account_exists(accounts, name)
	ret = {"name": name, "balance": round(accounts[name], 2)}
	return ret, 200

@app.post("/account/<name>/deposit")
def deposit(name):
	utils.verify_json(request)
	name = name.lower()
	utils.account_exists(accounts, name)
	amount = utils.get_amount(request)
	utils.positive_amount(amount)
	accounts[name] += amount
	return {"response": f'Successfully deposited {amount} into {name}\n'}, 200

@app.post("/account/<name>/withdraw")
def withdraw(name):
	utils.verify_json(request)
	name = name.lower()
	utils.account_exists(accounts, name)
	amount = utils.get_amount(request)
	utils.can_withdraw(accounts, name, amount)
	accounts[name] -= amount
	return {"response": f'Successfully withdrew {amount} from {name}\n'}, 200
