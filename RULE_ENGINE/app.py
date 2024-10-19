import streamlit as st
import ast

# Define the Node class for AST
class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left       # Reference to left child (Node)
        self.right = right     # Reference to right child (Node)
        self.value = value     # Operand value (used for conditions)

# Function to create a rule AST
def create_rule(rule_string):
    try:
        # Replace `AND` with `and` and `OR` with `or` for valid Python syntax
        rule_string = rule_string.replace("AND", "and").replace("OR", "or")
        
        parsed = ast.parse(rule_string, mode='eval')
        return convert_ast_to_node(parsed.body)
    except SyntaxError as e:
        st.error(f"Syntax Error in the rule: {e}")
        return None

def convert_ast_to_node(tree):
    if isinstance(tree, ast.BoolOp):
        if isinstance(tree.op, ast.And):
            return Node("operator", convert_ast_to_node(tree.values[0]), convert_ast_to_node(tree.values[1]), "AND")
        elif isinstance(tree.op, ast.Or):
            return Node("operator", convert_ast_to_node(tree.values[0]), convert_ast_to_node(tree.values[1]), "OR")
    elif isinstance(tree, ast.Compare):
        left = convert_ast_to_node(tree.left)
        right = convert_ast_to_node(tree.comparators[0])
        if isinstance(tree.ops[0], ast.Gt):
            return Node("operand", left, right, ">")
        elif isinstance(tree.ops[0], ast.Lt):
            return Node("operand", left, right, "<")
        elif isinstance(tree.ops[0], ast.Eq):
            return Node("operand", left, right, "==")
    elif isinstance(tree, ast.Name):
        return Node("variable", value=tree.id)
    elif isinstance(tree, ast.Constant):
        return Node("constant", value=tree.value)

# Combine rules function
def combine_rules(rules):
    combined = None
    for rule in rules:
        rule_ast = create_rule(rule)
        if combined is None:
            combined = rule_ast
        else:
            combined = Node("operator", combined, rule_ast, "AND")
    return combined

# Evaluate the AST function
def evaluate_rule(node, data):
    if node.type == "operator":
        left_val = evaluate_rule(node.left, data)
        right_val = evaluate_rule(node.right, data)
        if node.value == "AND":
            return left_val and right_val
        elif node.value == "OR":
            return left_val or right_val
    elif node.type == "operand":
        left_val = evaluate_rule(node.left, data)
        right_val = evaluate_rule(node.right, data)
        if node.value == ">":
            return left_val > right_val
        elif node.value == "<":
            return left_val < right_val
        elif node.value == "==":
            return left_val == right_val
    elif node.type == "variable":
        return data.get(node.value, None)
    elif node.type == "constant":
        return node.value

# Custom CSS to style the app
st.markdown("""
    <style>
    body {
        background-color: #f0f4f8;
    }
    .css-18e3th9 {
        padding: 1rem;
        background-color: #e6f7ff;
        border-radius: 10px;
    }
    .css-1d391kg {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 1rem;
    }
    h1, h2, h3 {
        color: #0073e6;
    }
    .stButton > button {
        background-color: #0073e6;
        color: white;
        border-radius: 10px;
        font-weight: bold;
    }
    .stTextInput > div > div > input {
        border: 2px solid #0073e6;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI
st.title("3-Tier Rule Engine Application")

# Input rule section
st.header("Create Rules")
rule_input = st.text_area("Enter a rule (e.g., age > 30 AND department == 'Sales')", height=100)
data_input = st.text_area("Enter user data (JSON format)", '{"age": 35, "department": "Sales", "salary": 60000, "experience": 3}', height=100)

# Parse the data input
try:
    data = eval(data_input)
except Exception as e:
    st.error(f"Error parsing input data: {e}")
    data = {}

# Button to create rule
if st.button("Create Rule"):
    if rule_input:
        rule_ast = create_rule(rule_input)
        if rule_ast:
            st.success(f"Rule created successfully!")
            st.json({"AST": rule_ast.__dict__})
    else:
        st.warning("Please enter a rule to create!")

# Combine rules section
st.header("Combine Rules")
rules_to_combine = st.text_area("Enter multiple rules (separate by newlines)", height=100).split("\n")

if st.button("Combine Rules"):
    if rules_to_combine:
        combined_ast = combine_rules(rules_to_combine)
        if combined_ast:
            st.success("Rules combined successfully!")
            st.json({"Combined AST": combined_ast.__dict__})
    else:
        st.warning("Please enter rules to combine!")

# Evaluate rule section
st.header("Evaluate Rule")
if st.button("Evaluate"):
    if rule_input and data:
        rule_ast = create_rule(rule_input)
        if rule_ast:
            result = evaluate_rule(rule_ast, data)
            st.success(f"Rule evaluation result: {result}")
    else:
        st.warning("Please enter both rule and user data for evaluation!")
