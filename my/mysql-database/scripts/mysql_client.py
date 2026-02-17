#!/usr/bin/env python3
"""
MySQL Database Client
Connects to MySQL and provides database inspection capabilities.
"""

import json
import sys
from typing import Dict, List, Any, Optional
import pymysql
from pymysql.cursors import DictCursor


class MySQLClient:
    """MySQL client for database operations."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize MySQL client with configuration."""
        self.config = config
        self.connection = None

    def connect(self):
        """Establish connection to MySQL database."""
        try:
            self.connection = pymysql.connect(
                host=self.config.get('host', 'localhost'),
                port=self.config.get('port', 3306),
                user=self.config['user'],
                password=self.config['password'],
                database=self.config.get('database'),
                charset='utf8mb4',
                cursorclass=DictCursor
            )
            return True
        except Exception as e:
            print(f"Connection error: {e}", file=sys.stderr)
            return False

    def disconnect(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()

    def list_databases(self) -> List[str]:
        """List all databases."""
        with self.connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES")
            return [row['Database'] for row in cursor.fetchall()]

    def list_tables(self, database: Optional[str] = None) -> List[str]:
        """List all tables in the specified or current database."""
        if database:
            self.connection.select_db(database)

        with self.connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            rows = cursor.fetchall()
            if not rows:
                return []

            key = next(iter(rows[0].keys()))
            return [row[key] for row in rows]

    def describe_table(self, table_name: str, database: Optional[str] = None) -> Dict[str, Any]:
        """Get detailed table structure including columns, indexes, and constraints."""
        if database:
            self.connection.select_db(database)

        result = {
            'table_name': table_name,
            'columns': [],
            'indexes': [],
            'foreign_keys': [],
            'create_statement': ''
        }

        with self.connection.cursor() as cursor:
            # Get column information
            cursor.execute(f"DESCRIBE `{table_name}`")
            result['columns'] = cursor.fetchall()

            # Get index information
            cursor.execute(f"SHOW INDEX FROM `{table_name}`")
            result['indexes'] = cursor.fetchall()

            # Get foreign key information
            cursor.execute(f"""
                SELECT
                    CONSTRAINT_NAME,
                    COLUMN_NAME,
                    REFERENCED_TABLE_NAME,
                    REFERENCED_COLUMN_NAME
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = DATABASE()
                    AND TABLE_NAME = %s
                    AND REFERENCED_TABLE_NAME IS NOT NULL
            """, (table_name,))
            result['foreign_keys'] = cursor.fetchall()

            # Get CREATE TABLE statement
            cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
            row = cursor.fetchone()
            if row:
                result['create_statement'] = list(row.values())[1]

        return result

    def execute_query(self, query: str) -> Dict[str, Any]:
        """Execute a SELECT query and return results."""
        with self.connection.cursor() as cursor:
            cursor.execute(query)

            if query.strip().upper().startswith('SELECT'):
                rows = cursor.fetchall()
                return {
                    'rows': rows,
                    'row_count': len(rows),
                    'columns': [desc[0] for desc in cursor.description] if cursor.description else []
                }
            else:
                self.connection.commit()
                return {
                    'affected_rows': cursor.rowcount,
                    'message': 'Query executed successfully'
                }


def load_config(config_path: str) -> Dict[str, Any]:
    """Load MySQL configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in config file: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: mysql_client.py <config_file> <command> [args...]", file=sys.stderr)
        print("\nCommands:", file=sys.stderr)
        print("  list-databases", file=sys.stderr)
        print("  list-tables [database]", file=sys.stderr)
        print("  describe-table <table_name> [database]", file=sys.stderr)
        print("  query <sql_query>", file=sys.stderr)
        sys.exit(1)

    config_file = sys.argv[1]
    command = sys.argv[2]

    config = load_config(config_file)
    client = MySQLClient(config)

    if not client.connect():
        sys.exit(1)

    try:
        if command == 'list-databases':
            databases = client.list_databases()
            print(json.dumps({'databases': databases}, indent=2))

        elif command == 'list-tables':
            database = sys.argv[3] if len(sys.argv) > 3 else None
            tables = client.list_tables(database)
            print(json.dumps({'tables': tables}, indent=2))

        elif command == 'describe-table':
            if len(sys.argv) < 4:
                print("Error: table_name required", file=sys.stderr)
                sys.exit(1)
            table_name = sys.argv[3]
            database = sys.argv[4] if len(sys.argv) > 4 else None
            info = client.describe_table(table_name, database)
            print(json.dumps(info, indent=2, default=str))

        elif command == 'query':
            if len(sys.argv) < 4:
                print("Error: SQL query required", file=sys.stderr)
                sys.exit(1)
            query = sys.argv[3]
            result = client.execute_query(query)
            print(json.dumps(result, indent=2, default=str))

        else:
            print(f"Unknown command: {command}", file=sys.stderr)
            sys.exit(1)

    except pymysql.MySQLError as e:
        print(f"MySQL error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        client.disconnect()


if __name__ == '__main__':
    main()
