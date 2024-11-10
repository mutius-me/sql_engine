test_cases = [
    # Test 1: Simple SELECT with a WHERE clause and integer comparison
    {
        "json_path": "tests/data/test_data_1.json",
        "queries": ["SELECT state FROM table WHERE population > 39538219", "exit"],
        "expected": ["Result #1:\n\tstate: California\n\n"]
    },

    # Test 2: SELECT with an equality condition
    {
        "json_path": "tests/data/test_data_1.json",
        "queries": ["SELECT state FROM table WHERE region = 'South'", "exit"],
        "expected": [
            "Result #1:\n\tstate: Texas\n\nResult #2:\n\tstate: Florida\n\n"
        ]
    },

    # Test 3: SELECT with a LIMIT clause
    {
        "json_path": "tests/data/test_data_1.json",
        "queries": ["SELECT state FROM table WHERE region = 'South' LIMIT 1", "exit"],
        "expected": ["Result #1:\n\tstate: Texas\n\n"]
    },

    # Test 4: Complex WHERE clause with AND operator
    {
        "json_path": "tests/data/test_data_1.json",
        "queries": ["SELECT state FROM table WHERE population > 20000000 AND region = 'West'", "exit"],
        "expected": ["Result #1:\n\tstate: California\n\n"]
    },

    # Test 5: Complex WHERE clause with OR operator
    {
        "json_path": "tests/data/test_data_1.json",
        "queries": ["SELECT state FROM table WHERE region = 'South' OR region = 'West'", "exit"],
        "expected": [
            "Result #1:\n\tstate: California\n\nResult #2:\n\tstate: Texas\n\nResult #3:\n\tstate: Florida"
        ]
    },

    # Test 7: SELECT with multiple conditions and nested parentheses
    {
        "json_path": "tests/data/test_data_2.json",
        "queries": ["SELECT name FROM table WHERE (age > 30 AND salary > 6500) OR (age < 10 AND region = 'North')", "exit"],
        "expected": [
            "Result #1:\n\tname: Alice\n\nResult #2:\n\tname: Bob\n\n",
        ]
    },

    # Test 7: SELECT with multiple conditions and nested parentheses
    {
        "json_path": "tests/data/test_data_2.json",
        "queries": ["SELECT name FROM table WHERE ((age > 30 AND salary > 6500) OR (age < 10 AND region = 'North')) AND name = 'Alice'", "exit"],
        "expected": [
            "Result #1:\n\tname: Alice\n\n",
        ]
    },


    # Test 8: Edge case with no matching rows
    {
        "json_path": "tests/data/test_data_2.json",
        "queries": ["SELECT name FROM table WHERE age > 100", "exit"],
        "expected": []
    },

    # Test 9: Testing case sensitivity in the WHERE clause (if not handled in the SQL engine)
    {
        "json_path": "tests/data/test_data_2.json",
        "queries": ["SELECT name FROM table WHERE region = 'south'", "exit"],
        "expected": []  # Assuming case sensitivity in SQL engine
    },

    # Test 10: Test with a string containing special characters
    {
        "json_path": "tests/data/test_data_3.json",
        "queries": ["SELECT description FROM table WHERE description = 'This is a @#$%ˆ&*test!'", "exit"],
        "expected": ["Result #1:\n\tdescription: This is a @#$%ˆ&*test!\n\n"]
    },

]
