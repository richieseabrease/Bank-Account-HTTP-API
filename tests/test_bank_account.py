# Tests
import random
import test_utils

## Create Account Tests

# test that we can create 1 account
def test_create_account(client):
	name = "account" + str(random.randrange(1,100000000))
	req = {"name": name}
	response = client.post("/account", json=req)
	result = response.get_json()

	assert result is not None
	assert response.status_code == 200
	assert "response" in result
	assert result["response"] == f'Successfully created account {name}\n'

# test that we can create multiple accounts
def test_create_multiple_accounts(client):
	for i in range(1000):
		name = "account" + str(random.randrange(1,100000000))
		req = {"name": name}
		response = client.post("/account", json=req)
		result = response.get_json()

		assert result is not None
		assert response.status_code == 200
		assert "response" in result
		assert result["response"] == f'Successfully created account {name}\n'

# test that the request must be json
def test_create_json(client):
	req  = "this is not json"
	response = client.post("/account", data=req)
	result = response.get_json()

	assert result is not None
	assert response.status_code == 400
	assert "error" in result
	assert result["error"] == "Request must be JSON"

# test that we cannot create an account without a name
def test_create_no_name(client):
	req = {"test": "field"}
	response = client.post("/account", json=req)
	result = response.get_json()

	assert result is not None
	assert response.status_code == 400
	assert "error" in result
	assert result["error"] == "name of account must be given"

# test that we cannot create an account with the same name
def test_duplicate_account(client):
	name = "account" + str(random.randrange(1,100000000))
	req = {"name": name}
	client.post("/account", json=req)

	response = client.post("/account", json=req)
	result = response.get_json()

	assert result is not None
	assert response.status_code == 400
	assert "error" in result
	assert result["error"] == "Account name already exists"

## Get Account Tests

# test that we can get a single created account
def test_get_account(client):
	name = test_utils.create_account(client)
	response = client.get(f'/account/{name}')
	result = response.get_json()

	assert result is not None
	assert response.status_code == 200
	assert "name" in result
	assert result["name"] == name
	assert "balance" in result
	assert result["balance"] == 0.0

# test that we can get multiple created accounts
def test_get_multiple_accounts(client):
	for i in range(1000):
		name = test_utils.create_account(client)
		response = client.get(f'/account/{name}')
		result = response.get_json()

		assert result is not None
		assert response.status_code == 200
		assert "name" in result
		assert result["name"] == name
		assert "balance" in result
		assert result["balance"] == 0.0

# test that we return 404 and empty response when account does not exist
def test_get_no_account(client):
	bad_name = "doesnt_exist"
	response = client.get(f'/account/{bad_name}')
	result = response.data

	assert result == b''
	assert response.status_code == 404

## Deposit Account Tests

# test the we can deposit to 1 account
def test_deposit(client):
	name = test_utils.create_account(client)
	req = { "amount": 5.0 }
	response = client.post(f'/account/{name}/deposit', json=req)
	result = response.get_json()
	new_amount = test_utils.get_account(client, name)

	assert result is not None
	assert response.status_code == 200
	assert "response" in result
	assert result["response"] == f'Successfully deposited 5.0 into {name}\n'
	assert new_amount["balance"] == 5.0

# test that we can deposit to multiple accounts
def test_multiple_deposits(client):
	for i in range(1000):
		name = test_utils.create_account(client)
		amount = round(random.uniform(1,100), 2)
		req = { "amount": amount }
		response = client.post(f'/account/{name}/deposit', json=req)
		result = response.get_json()
		new_amount = test_utils.get_account(client, name)

		assert result is not None
		assert response.status_code == 200
		assert "response" in result
		assert result["response"] == f'Successfully deposited {amount} into {name}\n'
		assert new_amount["balance"] == amount

# test that the input must be JSON
def test_deposit_not_json(client):
	req  = "this is not json"
	response = client.post("/account/name/deposit", data=req)
	result = response.get_json()

	assert result is not None
	assert response.status_code == 400
	assert "error" in result
	assert result["error"] == "Request must be JSON"

# test that we return 404 and empty response when account does not exist
def test_deposit_no_account(client):
	name = "doesnt_exist"
	req = { "amount": 5.0 }
	response = client.post(f'/account/{name}/deposit', json=req)
	result = response.data

	assert result == b''
	assert response.status_code == 404

# test that amount must be given
def test_deposit_no_amount(client):
	name = test_utils.create_account(client)
	req = {'this': 'field'}
	response = client.post(f'/account/{name}/deposit', json=req)
	result = response.get_json()

	assert result is not None
	assert response.status_code == 400
	assert "error" in result
	assert result["error"] == "amount must be given"

# test that amount must be > 0
def test_deposit_negative_amount(client):
	name = test_utils.create_account(client)
	req = {"amount": -5.5}
	response = client.post(f'/account/{name}/deposit', json=req)
	result = response.get_json()

	assert result is not None
	assert response.status_code == 400
	assert "error" in result
	assert result["error"] == "amount must be greater than 0"

## Withdraw Account Tests

# test that we can withdraw from 1 account
def test_withdraw(client):
	name = test_utils.create_account(client)
	test_utils.deposit_account(client, name, 10.00)
	req = {"amount": 5.0}
	response = client.post(f'/account/{name}/withdraw', json=req)
	result = response.get_json()
	new_amount = test_utils.get_account(client, name)

	assert result is not None
	assert response.status_code == 200
	assert "response" in result
	assert result["response"] == f'Successfully withdrew 5.0 from {name}\n'
	assert new_amount["balance"] == 5.0

# test that we can withdraw from multiple accounts
def test_withdraw_multiple(client):
	for i in range(1000):
		name = test_utils.create_account(client)
		dep_amount = round(random.uniform(100,200), 2)
		with_amount = round(random.uniform(1,99), 2)
		expected_amount = round(dep_amount - with_amount, 2)
		test_utils.deposit_account(client, name, dep_amount)
		req = {"amount": with_amount}
		response = client.post(f'/account/{name}/withdraw', json=req)
		result = response.get_json()
		new_amount = test_utils.get_account(client, name)

		assert result is not None
		assert response.status_code == 200
		assert "response" in result
		assert result["response"] == f'Successfully withdrew {with_amount} from {name}\n'
		assert new_amount["balance"] == expected_amount

# test that the input must be JSON
def test_withdraw_not_json(client):
	req  = "this is not json"
	response = client.post("/account/name/withdraw", data=req)
	result = response.get_json()

	assert result is not None
	assert response.status_code == 400
	assert "error" in result
	assert result["error"] == "Request must be JSON"

# test that we return 404 and empty response when account does not exist
def test_withdraw_no_account(client):
	name = "doesnt_exist"
	req = { "amount": 5.0 }
	response = client.post(f'/account/{name}/withdraw', json=req)
	result = response.data

	assert result == b''
	assert response.status_code == 404

# test that amount must be given
def test_withdraw_no_amount(client):
	name = test_utils.create_account(client)
	req = {'this': 'field'}
	response = client.post(f'/account/{name}/withdraw', json=req)
	result = response.get_json()

	assert result is not None
	assert response.status_code == 400
	assert "error" in result
	assert result["error"] == "amount must be given"

# test that we cannot withdraw more than account balance
def test_withdraw_more_than_balance(client):
	name = test_utils.create_account(client)
	test_utils.deposit_account(client, name, 10.00)
	req = {"amount": 50.0}
	response = client.post(f'/account/{name}/withdraw', json=req)
	result = response.get_json()

	assert result is not None
	assert response.status_code == 400
	assert "error" in result
	assert result["error"] == "amount must be less than the account balance"

## Complete Tests

# test that we can withdraw and deposit multiple times
def test_complete(client):
	name = test_utils.create_account(client)
	test_utils.deposit_account(client, name, 10.00)
	test_utils.withdraw_account(client, name, 5.0)
	test_utils.deposit_account(client, name, 2.25)
	test_utils.deposit_account(client, name, 1.10)
	test_utils.withdraw_account(client, name, 4.36)
	test_utils.withdraw_account(client, name, 1.02)
	test_utils.deposit_account(client, name, 6.74)
	new_amount = test_utils.get_account(client, name)

	assert new_amount["balance"] == 9.71

# test that we can withdraw and deposit multiple times from multiple accounts
def test_complete_multiple(client):
	name1 = test_utils.create_account(client)
	name2 = test_utils.create_account(client)
	test_utils.deposit_account(client, name1, 10.0)
	test_utils.deposit_account(client, name2, 3.45)
	test_utils.withdraw_account(client, name1, 7.25)
	test_utils.withdraw_account(client, name2, 1.1)
	test_utils.deposit_account(client, name2, 15.24)
	test_utils.withdraw_account(client, name1, 2.03)
	new_amount1 = test_utils.get_account(client, name1)
	new_amount2 = test_utils.get_account(client, name2)

	assert new_amount1["name"] == name1
	assert new_amount1["balance"] == 0.72
	assert new_amount2["name"] == name2
	assert new_amount2["balance"] == 17.59