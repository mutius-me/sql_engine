import re
from typing import List
from .where import build_tree, evaluate_tree

class SQLEngine:
    """
    A SQL Engine built to handle basic SQL querying.
    """

    def __init__(self, json_array):
        self.data = json_array
        self.original_ordering = {id(obj): i for i, obj in enumerate(json_array)}


    def query(self, query):
        # Parse query into clauses
        parsed_input = self._parse(query)
        filtered_data = [obj for obj in self.data]

        # We ignore the FROM clause because we assume the table is the JSON file called as an argument to main.
        if parsed_input['WHERE'] is not None:
            filtered_data = self._process_where_clause(parsed_input['WHERE'], filtered_data)
        if parsed_input['LIMIT'] is not None:
            filtered_data = self._process_limit_clause(parsed_input['LIMIT'], filtered_data)
        filtered_data = self._process_select_clause(parsed_input['SELECT'], filtered_data)

        return filtered_data

    @staticmethod
    def _parse(query):
        pattern = r"""
                SELECT\s+(.*?)\s+FROM\s+(.*?)(?:\s+|$)
                (?:WHERE\s+(.*?)\s*)?
                (?:LIMIT\s+(\d+)\s*)?
                $
            """

        match = re.search(pattern, query, re.IGNORECASE | re.VERBOSE)

        if match:
            return {
                'SELECT': match.group(1).strip(),
                'FROM': match.group(2).strip(),
                'WHERE': match.group(3).strip() if match.group(3) else None,
                'LIMIT': match.group(4).strip() if match.group(4) else None
            }
        else:
            raise ValueError("Invalid SQL query")


    def _process_where_clause(self, clause: str, filtered_data: List[dict]) -> List[dict]:
        root = build_tree(clause)
        filtered_data = evaluate_tree(root, filtered_data)

        # Ensure the filtered ordering matches the original ordering
        filtered_data.sort(key=lambda obj: self.original_ordering[id(obj)])
        return filtered_data

    @staticmethod
    def _process_limit_clause(clause: str, filtered_data: List[dict]) -> List[dict]:
        limit = int(clause)
        return filtered_data[:limit]

    @staticmethod
    def _process_select_clause(clause: str, filtered_data: List[dict]) -> List[dict]:
        if clause == '*':
            return filtered_data
        else:
            fields = [field.strip() for field in clause.split(',')]
            result = []
            for obj in filtered_data:
                selected = {field: obj[field] for field in fields if field in obj}
                result.append(selected)
            return result
