import pytest
import bank_account
import bank_account_v2

@pytest.fixture
def client():
    bank_account.app.config['TESTING'] = True
    client = bank_account.app.test_client()
    yield client
