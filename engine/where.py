import re
from typing import Optional, List

class TreeNode:
    """
    A binary tree node used to represent simple and compound expressions
    in a (simplified) SQL WHERE clause.
    """
    def __init__(self, value, left=None, right=None):
        self.value = value  # 'AND', 'OR', or 'exp' (leaf node condition)
        self.left = left
        self.right = right

    def __repr__(self):
        if not self.left and not self.right:
            return f"{self.value}"
        return f"({self.left} {self.value} {self.right})"

def build_tree(expression: str) -> TreeNode:
    """
    # Builds a binary tree representation of a (simplified) SQL WHERE clause.
    """
    stack = []
    current_node = None
    i = 0
    n = len(expression)

    def is_logical_operator(sub_exp):
        return sub_exp == "AND" or sub_exp == "OR"

    # Main parsing loop: builds binary tree in one pass, O(n)
    while i < n:

        # Handles nested expressions
        if expression[i] == '(':
            stack.append(current_node)
            current_node = None
            i += 1

        elif expression[i] == ')':
            last_node = stack.pop()
            if last_node is not None:
                if last_node.left is None:
                    last_node.left = current_node
                else:
                    last_node.right = current_node
                current_node = last_node
            i += 1

        # Extract logical operators
        elif (i + 3 <= n and expression[i:i + 3] == 'AND') or (i + 2 <= n and expression[i:i + 2] == 'OR'):
            operator = expression[i:i+3] if expression[i:i+3] == 'AND' else expression[i:i+2]
            i += len(operator)

            new_node = TreeNode(operator)
            new_node.left = current_node
            current_node = new_node

        # Extract leaf-level expressions (e.g., "age > 29")
        else:
            start_idx = i

            while i < n and expression[i] not in '()' and not is_logical_operator(expression[i:i+3].strip()):
                i += 1

            exp = expression[start_idx:i].strip()

            leaf_node = TreeNode(exp)

            if current_node is None:
                current_node = leaf_node
            else:
                current_node.right = leaf_node

        while i < n and expression[i] == ' ':
            i += 1

    return current_node

def filter_by_expression(data: Optional[List[dict]], expression: str) -> List[dict]:
    """
    Given a list of JSON objects and a leaf-level conditional expression (e.g., age = 30),
    filters out JSON objects that do not fulfill the condition. Returns the filtered list.
    """

    if not data:
        return []

    match = re.match(r"(\S+)\s*(=|!=|<|>)\s*(\".*?\"|'.*?'|\S+)", expression)
    if not match:
        raise ValueError(f"Invalid expression format: {expression}")

    key, operator, filter_value = match.groups()
    key = key.strip()
    filter_value = filter_value.strip()

    is_numeric = re.fullmatch(r'-?\d+(\.\d+)?', filter_value) is not None

    if is_numeric:
        filter_value = float(filter_value) if '.' in filter_value else int(filter_value)
    else:
        if filter_value.startswith(("'", '"')) and filter_value.endswith(("'", '"')):
            filter_value = filter_value[1:-1]

    filtered_data = []
    for obj in data:
        if key not in obj:
            continue

        field_value = obj[key]

        if is_numeric:
            if isinstance(field_value, str) and re.fullmatch(r'-?\d+(\.\d+)?', field_value):
                field_value = float(field_value) if '.' in field_value else int(field_value)
            elif not isinstance(field_value, (int, float)):
                continue

        match operator:
            case '=':
                if field_value == filter_value:
                    filtered_data.append(obj)
            case '!=':
                if field_value != filter_value:
                    filtered_data.append(obj)
            case '<':
                if is_numeric and field_value < filter_value:
                    filtered_data.append(obj)
            case '>':
                if is_numeric and field_value > filter_value:
                    filtered_data.append(obj)

    return filtered_data

def evaluate_tree(node: TreeNode, filtered_data: Optional[List[dict]] = None) -> List[dict]:
    """
    Recursively evaluates the WHERE clause binary tree,
    returning a filtered list of JSON objects.
    """

    # O(n) implementations of list intersection and list union
    def intersection(list1: List[dict], list2: List[dict]) -> List[dict]:
        list2_ids = set(id(obj) for obj in list2)
        return [item for item in list1 if id(item) in list2_ids]

    def union(list1: List[dict], list2: List[dict]) -> List[dict]:
        list1_ids = set(id(obj) for obj in list1)
        list1.extend(item for item in list2 if id(item) not in list1_ids)
        return list1

    if filtered_data is None or node is None:
        return []

    if node.value == 'AND':
        left_results = evaluate_tree(node.left, filtered_data)
        right_results = evaluate_tree(node.right, filtered_data)
        return intersection(left_results, right_results)

    elif node.value == 'OR':
        # Perform union for OR
        left_results = evaluate_tree(node.left, filtered_data)
        right_results = evaluate_tree(node.right, filtered_data)
        return union(left_results, right_results)

    else:
        return filter_by_expression(filtered_data, node.value)
