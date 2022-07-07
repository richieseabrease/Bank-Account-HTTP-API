# Utility functions to use in tests
import random

def create_account(client):
	name = "account" + str(random.randrange(1,100000000))
	req = {"name": name}
	client.post("/account", json=req)
	return name

def get_account(client, name):
	response = client.get(f'/account/{name}')
	return response.get_json()

def deposit_account(client, name, amount):
	req = {"amount": amount}
	client.post(f'/account/{name}/deposit', json=req)

def withdraw_account(client, name, amount):
	req = {"amount": amount}
	client.post(f'/account/{name}/withdraw', json=req)