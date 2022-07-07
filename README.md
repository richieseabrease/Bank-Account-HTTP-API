# Bank Account HTTP API

## Description

In this project, I created a bank account system as an HTTP API. I created two separate version of this system, with the main difference between version 1 and version 2 being the backing store that keeps track of the account information. 

The Flask Framework was used to handle the HTTP requests. This framework was chosen because it is lightweight, simple to use and easy to setup. Using flask, I created functions that map to the 4 defined endpoints. These functions call out to various utility functions to perform validation and transformation on the data given. 

The prompt only specified 2 error cases, but I added in some extra error checking, such as ensuring the data in the request is JSON, deposit amount is greater than 0, withdraw amount is less than the balance, and more. If any of the validation fails, an error is raised and I use Flask's error handler to cleanly return an error message and http code. If all validation is complete then, depending on the request, the backing storage is either updated or retrieved as needed.

In Version 1, I used python's dictionary to hold all of the data. This created a clear key-value mapping from unique account name to the balance. This allows us to store and lookup the data relatively quickly, but it keeps all of the data in memory which is not great for large data sets or long term storage. 

In Version 2, I used SQLite as the backing store. I created a sqlite databse with 2 columns, name and balance. This allows us to organize the data in a long term storage space, that can do lookups relatively quickly on large data sets, but it is slower on smaller data sets. 

The main code is under `bank_account.py` with some utility functions in `utils.py`. The SQLite Database code is `sqlite_db.py`. `invalid_usage.py` contains the code for handling exceptions and validation failures.

I also included a suite of tests using pytest, all located under the directory `tests/`. I setup a testing client to test various functionality pieces of the HTTP API. I make every API call defined, and hit all error cases.

## How to Build and Run
I've included a Pipfile to allow easy installation of all dependencies. If using pipenv, dependencies can be installed by running `pipenv install`. This was written using Python 3, specifically 3.8. The dependencies required are flask, and pytest. 
To run version 1, perform the following commands:
```
export FLASK_APP=bank_account
flask run
```
To run version 2, perform the following commands:
```
export FLASK_APP=bank_account_v2
flask run
```
This will create an HTTP Server listening on localhost to which you can then make the API calls against.
To run the tests run `python -m pytest -s`. To run the tests against version 2, edit `tests/conftest.py` changing `bank_account` to `bank_account_v2` and then running `python -m pytest -s`
