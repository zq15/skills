---
name: mysql-database
description: "Connect to MySQL databases to inspect schemas, explore table structures, and execute queries. Use when Claude needs to: (1) View all databases or tables in a MySQL instance, (2) Examine table structure including columns, data types, indexes, and foreign keys, (3) Execute SELECT queries to retrieve data, (4) Understand database schema and relationships. Works with configuration files for secure credential management."
---

# MySQL Database

Connect to and inspect MySQL databases to understand schemas, table structures, and data.

## Quick Start

1. **Create configuration file** with your MySQL credentials (based on `assets/mysql_config.example.json`)
2. **Install dependencies**: `pip install -r scripts/requirements.txt`
3. **Run commands** using the `mysql_client.py` script

## Configuration

Create a JSON configuration file with your MySQL connection details:

```json
{
  "host": "localhost",
  "port": 3306,
  "user": "your_username",
  "password": "your_password",
  "database": "your_default_database"
}
```

The `database` field is optional. If not specified, you can provide the database name in individual commands.

For first-time connectivity checks (for example, `list-databases`), leave `database` unset to avoid failures when a default schema does not exist.

## Available Commands

### List All Databases

View all databases accessible with the provided credentials:

```bash
python scripts/mysql_client.py config.json list-databases
```

Returns JSON with database names:
```json
{
  "databases": ["db1", "db2", "db3"]
}
```

### List Tables

View all tables in a database:

```bash
# Use database from config
python scripts/mysql_client.py config.json list-tables

# Specify database explicitly
python scripts/mysql_client.py config.json list-tables my_database
```

Returns JSON with table names:
```json
{
  "tables": ["users", "orders", "products"]
}
```

### Describe Table Structure

Get comprehensive table structure including columns, indexes, and foreign keys:

```bash
# Use database from config
python scripts/mysql_client.py config.json describe-table users

# Specify database explicitly
python scripts/mysql_client.py config.json describe-table users my_database
```

Returns detailed JSON with:
- **columns**: Field names, types, null constraints, keys, defaults, and extra attributes
- **indexes**: Index names, columns, uniqueness, and type
- **foreign_keys**: Foreign key constraints and referenced tables
- **create_statement**: Full CREATE TABLE statement

Example output:
```json
{
  "table_name": "users",
  "columns": [
    {
      "Field": "id",
      "Type": "int(11)",
      "Null": "NO",
      "Key": "PRI",
      "Default": null,
      "Extra": "auto_increment"
    },
    {
      "Field": "email",
      "Type": "varchar(255)",
      "Null": "NO",
      "Key": "UNI",
      "Default": null,
      "Extra": ""
    }
  ],
  "indexes": [...],
  "foreign_keys": [...],
  "create_statement": "CREATE TABLE `users` ..."
}
```

### Execute Query

Execute SELECT queries to retrieve data:

```bash
python scripts/mysql_client.py config.json query "SELECT * FROM users LIMIT 10"
```

Returns JSON with query results:
```json
{
  "rows": [
    {"id": 1, "email": "user@example.com", "name": "John"},
    {"id": 2, "email": "user2@example.com", "name": "Jane"}
  ],
  "row_count": 2,
  "columns": ["id", "email", "name"]
}
```

**Note**: Only SELECT queries are recommended. Modify operations (INSERT, UPDATE, DELETE) will execute but should be used cautiously.

## Workflow Examples

### Understanding a New Database

When exploring an unfamiliar database:

1. List all databases to identify the target
2. List tables in the database to see available data
3. Describe key tables to understand structure
4. Run sample queries to examine actual data

### Answering Schema Questions

When users ask "What's in the database?" or "Show me the user table structure":

1. Use `list-tables` to show available tables
2. Use `describe-table` to show detailed structure
3. Reference the CREATE statement for exact DDL

### Exploring Relationships

When understanding table relationships:

1. Use `describe-table` to get foreign key information
2. Check the `foreign_keys` array for references
3. Describe related tables to see the full relationship

## Security Notes

- Store configuration files securely and never commit them to version control
- Use read-only database credentials when possible
- The script supports all SQL commands, but focus on SELECT queries for safety
- Configuration files may contain sensitive credentials

## Resources

- **scripts/mysql_client.py**: Python client for MySQL operations
- **scripts/requirements.txt**: Python dependencies (pymysql)
- **assets/mysql_config.example.json**: Template configuration file
