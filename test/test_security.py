import os
import pytest
from src.utils.security import get_secure_input, get_credentials
from unittest.mock import patch

def test_get_secure_input_with_env():
    with patch.dict(os.environ, {'TEST_VAR': 'test_value'}):
        result = get_secure_input("Test: ", env_var='TEST_VAR')
        assert result == 'test_value'

@patch('getpass.getpass')
def test_get_secure_input_without_env(mock_getpass):
    mock_getpass.return_value = 'test_input'
    result = get_secure_input("Test: ")
    assert result == 'test_input'

@patch('builtins.input')
@patch('getpass.getpass')
def test_get_credentials(mock_getpass, mock_input):
    mock_input.return_value = 'test_user'
    mock_getpass.return_value = 'test_pass'
    username, password = get_credentials()
    assert username == 'test_user'
    assert password == 'test_pass'
