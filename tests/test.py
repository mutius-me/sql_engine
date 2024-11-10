import pytest
from unittest.mock import patch
from main import main  # Adjust this import as necessary
from test_cases import test_cases

@pytest.mark.parametrize("test_case", test_cases)
def test_query_engine(test_case, capsys, monkeypatch):

    # Set up mock inputs
    test_args = ["main.py", test_case["json_path"]]
    monkeypatch.setattr('sys.argv', test_args)

    # Use patch to simulate user input for SQL queries
    with patch('builtins.input', side_effect=test_case["queries"]):
        main()

    captured = capsys.readouterr()

    for expected_output in test_case["expected"]:
        assert expected_output in captured.out