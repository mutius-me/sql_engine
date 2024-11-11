# SQL Engine
This is a Python implementation of a simple SQL engine that supports SQL querying on a flat JSON array. The engine supports binary conditions `=`, `!=`, `<`, `>`, `AND`, `OR`, parentheses, and literals. It assumes the JSON array contains JSON objects with identical keys, and assumes well-formatted inputted queries.

## To run as a binary:
- Navigate to `sql_engine/dist/`.
- Run `./main <file_path_here.json>`.
- Pass in SQL queries as standard input.


## To run as a Python script:
- Install `uv` using `pip install uv`.
- Run `uv sync`.
- Run `p main.py <file_path_here.json>`.
- Pass in SQL queries as standard input.
