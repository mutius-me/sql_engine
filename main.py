import argparse
import json
from engine.engine import SQLEngine

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('json_file', type=str, help='Path to the JSON file containing the data')
    args = arg_parser.parse_args()

    json_array = load_json_data(args.json_file)
    sql_engine = SQLEngine(json_array)

    try:
        while True:
            sql_query = input("Enter SQL query (or type 'exit' to quit): ")
            if sql_query.lower() == 'exit':
                break

            result = sql_engine.query(sql_query)
            for i, item in enumerate(result):
                print(f"Result #{i + 1}:")
                for key, value in item.items():
                    print(f"\t{key}: {value}")
                print()


    except KeyboardInterrupt:
        print("\nExiting program...")

def load_json_data(filepath):
    """Load and return the data from a JSON file."""
    with open(filepath, 'r') as file:
        return json.load(file)

if __name__ == '__main__':
    main()