# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project called "dataverse-proj" that appears to be in early development stages. The project uses modern Python packaging with `pyproject.toml` and requires Python 3.11+.

## Project Structure

```
dataverse_proj/
├── main.py                      # Entry point
├── src/
│   ├── dataverse_client.py     # Main Dataverse client with authentication and schema methods
│   └── examples/
│       ├── basic_connection.py # Basic connection and authentication example
│       └── schema_retrieval.py # Table schema retrieval example
├── test/                       # Test directory
├── notebooks/                  # Jupyter notebooks directory
├── data/                       # Data directory
├── docs/                       # Documentation directory
├── requirements.txt            # Python dependencies (msal, requests)
├── .env.example               # Environment variables template
├── pyproject.toml             # Python project configuration
└── README.md                  # Project readme
```

## Development Commands

This project uses `uv` for dependency management:

```bash
# Install dependencies
uv pip install -r requirements.txt

# Run the main application
python main.py

# Run examples
python src/examples/basic_connection.py
python src/examples/schema_retrieval.py

# Install the project in development mode
uv pip install -e .
```

## Dataverse Client

The main functionality is provided by `DataverseClient` class in `src/dataverse_client.py`:

### Authentication
- Uses Microsoft Authentication Library (MSAL) for client secret authentication
- Supports environment variables: `DATAVERSE_CLIENT_ID`, `DATAVERSE_CLIENT_SECRET`, `DATAVERSE_TENANT_ID`, `DATAVERSE_ENVIRONMENT_URL`
- Implements token caching and automatic refresh

### Schema Methods
- `get_table_schema(table_name)` - Get complete schema for a specific table
- `list_tables()` - List all available tables in the environment
- `get_table_attributes(table_name)` - Get detailed column definitions
- `test_connection()` - Verify authentication and connectivity

### Configuration
1. Copy `.env.example` to `.env` and fill in your credentials
2. Or set environment variables directly
3. Azure AD app registration requires Dataverse permissions

## Architecture Notes

- Uses modern Python packaging with `pyproject.toml` (Python 3.11+)
- Client uses MSAL for secure OAuth 2.0 authentication
- Implements retry logic and proper error handling
- Follows Microsoft's recommended patterns for Dataverse API access