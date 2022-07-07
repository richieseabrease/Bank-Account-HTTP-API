import sqlite3

def init_db():
	connection = sqlite3.connect('bank_account.db')
	cur = connection.cursor()
	cur.execute("DROP TABLE IF EXISTS bank_accounts")
	cur.execute("CREATE TABLE bank_accounts (name TEXT,balance REAL)")
	connection.commit()
	connection.close()

def create_account(name):
	connection = sqlite3.connect('bank_account.db')
	cur = connection.cursor()
	cur.execute("INSERT INTO bank_accounts VALUES (?, ?)", (name, 0.0))
	connection.commit()
	connection.close()

def get_account(name):
	connection = sqlite3.connect('bank_account.db')
	cur = connection.cursor()
	row = cur.execute("SELECT * FROM bank_accounts WHERE name = ?", (name,)).fetchone()
	connection.close()
	return row

def update_balance(name, balance):
	connection = sqlite3.connect('bank_account.db')
	cur = connection.cursor()
	cur.execute("UPDATE bank_accounts SET balance = ? WHERE name = ?", (balance, name))
	connection.commit()
	connection.close()
