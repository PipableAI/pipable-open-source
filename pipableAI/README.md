# PipableAI 🚀

## About

PipableAI is a Python package that simplifies the process of querying a database. It provides a high-level interface for connecting to a remote database server, generating and executing natural language-based data search queries mapped to database queries using a language model.

## Current Features

- **Natural Language Queries**: Express database queries in plain English.
- **PostgreSQL Integration**: Seamlessly connects to PostgreSQL databases.
- **Language Model Mapping**: Translates natural language queries into SQL queries.
- **Structured Results**: Returns query results in a structured format for easy processing.

## Installation

To install PipableAI, you can use `pip3`, Python's package manager. Open your terminal or command prompt and run the following command:

```bash
pip3 install pipableai
```

**Note:** PipableAI requires Python 3.7 or higher.

If you prefer to install PipableAI from source, you can clone the GitHub repository and install it using `setup.py`. Navigate to the project directory and run:

```bash
python3 setup.py install
```

This will install PipableAI locally on your system.

## Usage

PipableAI simplifies the process of connecting to a remote db servers, generating SQL queries using a language model, and executing them. This section provides a step-by-step guide on how to use PipableAI effectively in your Python projects.

### Import Pipable:

To start using PipableAI, import the necessary classes:

```python
from pipableai import Pipable
from pipableai.llm_client.pipllm import PipLlmApiClient
from pipableai.core.postgresql_connector import PostgresConfig, PostgresConnector
```

### Initialize Pipable:

Create an instance of Pipable by providing the required database configuration and LLM API base URL:

```python
# Define PostgreSQL configuration
postgres_config = PostgresConfig(
    host="your_postgres_host",
    port=5432,  # Replace with your port number
    database="your_database_name",
    user="your_username",
    password="your_password",
)

# Initialize the database connector and LLM API client
database_connector = PostgresConnector(postgres_config)
llm_api_client = PipLlmApiClient(api_base_url="https://your-pipllm-api-url.com")

# Create a Pipable instance
pipable_instance = Pipable(database_connector=database_connector, llm_api_client=llm_api_client)
```

### Generate and Execute Queries:

Generate SQL queries using the language model and execute them on the database.
For Better Performance one can pass the tables names which shold be used in the query

#### When `table_names` is None or not passed in:

```python
question = "List all employees."

# Generate the query
try:
    result_df = pipable_instance.ask(question)
    print("Query Result:")
    print(result_df)
except Exception as e:
    print(f"Error: {e}")

# Generate and execute the query
try:
    result_df = pipable_instance.ask_and_execute(question)
    print("Query Result:")
    print(result_df)
except Exception as e:
    print(f"Error: {e}")

```

#### When `table_names` is populated with correct table names:

```python
table_names = ["table1", "table2", "table3"]
question = "List all employees."

# Generate and execute the query
try:
    result_df = pipable_instance.ask_and_execute(question, table_names)
    print("Query Result:")
    print(result_df)
except Exception as e:
    print(f"Error: {e}")

table_names = ["table1", "table2", "table3"]
question = "List all employees."

# Generate the query
try:
    result_query = pipable_instance.ask(question, table_names)
    print("Query Result:")
    print(result_query)
except Exception as e:
    print(f"Error: {e}")
```
#### When `table_names` is an empty list:

```python
table_names = []
question = "List all employees."

# Generate and execute the query
try:
    result_df = pipable_instance.ask_and_execute(question, table_names)
    print("Query Result:")
    print(result_df)
except Exception as e:
    print(f"Error: {e}")
```

Handle exceptions appropriately to ensure graceful error handling in your application.

### Disconnect from the Database:

Close the connection to the PostgreSQL server after executing the queries:

```python
pipable_instance.disconnect()
```

or

```python
database_connector.disconnect()
```

Ensure that you disconnect from the database to release resources when the queries are completed.

### Additional Information:

- Check the interfaces: `DatabaseConnectorInterface` and `LlmApiClientInterface` for more details on the methods and functionalities provided by Pipable.

## Example

For a complete example, refer to the `example/` directory in this repository.

## Documentation

For detailed usage instructions and examples, please refer to the [official documentation](https://pipableai.github.io/pipable-docs/).

## Contributing

We welcome contributions from the community! To contribute to Pipable, follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature-name`
3. Make changes and commit: `git commit -m 'Description of changes'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

Please read our [Contribution Guidelines](https://github.com/PipableAI/pipable-open-source/blob/main/pipableAI/CONTRIBUTING.md) for more details.

## License

This project is licensed under the Apache 2.0 - see the [LICENSE](https://github.com/PipableAI/pipable-open-source/blob/main/pipableAI/LICENSE) file for details.

---