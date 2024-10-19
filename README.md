                                        **  3-Tier Rule Engine Application **
                                        
** Project Overview**

This project implements a 3-tier rule engine application to dynamically create, combine, and evaluate user eligibility rules based on attributes such as age, department, income, and experience. The application uses Abstract Syntax Trees (AST) to represent rules, allowing for dynamic modification and combination of conditions. The application provides a simple UI for rule creation, rule combination, and rule evaluation using Streamlit and can be extended with additional features.

Features
Create Rules: Generate ASTs from conditional rule strings.
Combine Rules: Combine multiple rule ASTs using logical operators (AND, OR).
Evaluate Rules: Evaluate user data against defined rules to determine eligibility.
Customizable: Supports dynamic rule modification.
Error Handling: Handles syntax errors and missing data.
Tech Stack
Frontend: Streamlit
Backend: Python (AST manipulation)
Database: (Optional) PostgreSQL/SQLite for storing rules
Containerization: Docker (Optional)
Installation Instructions
Prerequisites
Ensure you have the following installed:

Python 3.9 or higher
Pip (Python package manager)
Docker (optional for containerization)
Setup Steps
Clone the repository:

bash
git clone https://github.com/GogulaPavan/RULE_ENGINE.git
cd 3-tier-rule-engine
Install dependencies:

Install the required Python packages using the following command:

bash

pip install -r requirements.txt
Run the application:

Run the Streamlit application locally:

bash

streamlit run app.py
The application will be accessible at http://localhost:8501.

Docker Setup (Optional)
If you prefer to run the application using Docker:

Build the Docker image:

bash
docker build -t rule-engine-app .
Run the Docker container:

bash
docker run -p 8501:8501 rule-engine-app
API Endpoints (Optional)
If you have API functionality, here’s an example API design:

POST /api/create_rule
Request body: {"rule_string": "age > 30 AND department == 'Sales'"}
Response: AST representation of the rule.
POST /api/combine_rules
Request body: {"rules": ["rule1", "rule2"]}
Response: Combined AST of the rules.
POST /api/evaluate
Request body: {"ast": {...}, "data": {"age": 35, "department": "Sales"}}
Response: True or False depending on the evaluation.
Design Choices
AST Design
The core of the rule engine is built on an Abstract Syntax Tree (AST), which represents logical rules and conditions. The AST is structured as follows:

Node Types:
Operator: Represents logical operators like AND, OR.
Operand: Represents conditions (e.g., age > 30, salary < 50000).
Each node in the AST is either an operator or an operand and connects to its left and right child nodes.

Rule Parsing
The application parses rule strings like age > 30 AND department == 'Sales' into an AST. The Python ast module is used to parse and convert these expressions into the custom Node structure, allowing for flexible and dynamic evaluation of rules.

Error Handling
The rule engine has built-in error handling for:

Invalid Rule Syntax: Catches syntax errors in the input rule string.
Missing Data: Handles missing attributes gracefully when evaluating rules against user data.
Database Schema (Optional)
If you are using a database to store the rules, here's an example schema for PostgreSQL/SQLite:

sql
CREATE TABLE rules (
    id SERIAL PRIMARY KEY,
    rule_string TEXT,
    ast_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
You can store the original rule string and its corresponding AST representation in JSON format.

How to Use the Application
Create a Rule:

Enter a rule string (e.g., age > 30 AND department == 'Sales') in the provided input field and click on Create Rule.
The AST representation of the rule will be generated and displayed.
Combine Rules:

Input multiple rule strings (each on a new line) and click Combine Rules. The rules will be logically combined using the AND operator.
Evaluate a Rule:

Enter a rule string and provide user data in JSON format (e.g., {"age": 35, "department": "Sales", "salary": 60000}). Click Evaluate to determine whether the user satisfies the rule conditions.
Tests
You can run unit tests to verify the logic of the AST creation, combination, and evaluation.

Install pytest:

bash

pip install pytest
Run tests:

bash
pytest tests/
Tests cover the following:

AST creation from rule strings
Rule combination logic
Evaluation of rules against user data
Dependencies
Streamlit: For building the web UI.
AST: Python module for parsing rule strings.
Docker (Optional): For containerizing the application.
Install the dependencies using:

bash
pip install -r requirements.txt
Future Enhancements
Dynamic Rule Modifications: Extend the rule engine to allow for modification of existing rules.
Database Integration: Store and retrieve rules from a database.
Advanced Conditions: Support for user-defined functions within rules for more complex conditions.

Contact
For any questions or issues, please reach out to:

GitHub: GogulaPavan
Email: gogulapavan970@gmail.com
This README.md provides a comprehensive guide to running, understanding, and extending the project.
