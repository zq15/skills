---
name: nacos-config
description: "Read and search Nacos configuration files via HTTP API. Use when Claude needs to: (1) View all configuration files in a Nacos namespace, (2) Read the content of specific configuration files (e.g., application-local.yml), (3) Search for configurations by dataId or group name, (4) Work with Nacos configuration management system. Supports customizable namespace IDs, group names, and Nacos server URLs."
---

# Nacos Config

Read and manage Nacos configuration files through the Nacos v3 Admin API.

## Overview

This skill provides two Python scripts for interacting with Nacos configuration:

1. **list_configs.py** - List all configurations in a namespace, with optional search filtering
2. **get_config.py** - Retrieve the content of a specific configuration file

Both scripts use Python's built-in urllib, requiring no additional dependencies.

## Quick Start

List all configurations in the default namespace:

```bash
scripts/list_configs.py
```

Get a specific configuration file:

```bash
scripts/get_config.py application-local.yml
```

## List All Configurations

Use `list_configs.py` to view all configuration files in a namespace.

**Basic usage:**

```bash
scripts/list_configs.py
```

**Search for specific configurations:**

```bash
scripts/list_configs.py --search application
```

**Custom namespace:**

```bash
scripts/list_configs.py --namespace-id YOUR_NAMESPACE_ID
```

**JSON output:**

```bash
scripts/list_configs.py --format json
```

**Full options:**

```bash
scripts/list_configs.py \
  --base-url http://localhost:8848 \
  --namespace-id 14b39079-899b-4ca5-af43-a9339a69dfbf \
  --search application \
  --format table
```

## Get Specific Configuration

Use `get_config.py` to retrieve the content of a specific configuration file.

**Basic usage (returns raw config content):**

```bash
scripts/get_config.py application-local.yml
```

**Specify group:**

```bash
scripts/get_config.py application-local.yml --group MY_GROUP
```

**JSON output with metadata:**

```bash
scripts/get_config.py application-local.yml --format json
```

**Custom namespace:**

```bash
scripts/get_config.py application-local.yml --namespace-id YOUR_NAMESPACE_ID
```

**Full options:**

```bash
scripts/get_config.py application-local.yml \
  --base-url http://localhost:8848 \
  --namespace-id 14b39079-899b-4ca5-af43-a9339a69dfbf \
  --group DEFAULT_GROUP \
  --format content
```

## Configuration Options

Both scripts support the following configuration parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--base-url` | `http://localhost:8848` | Nacos server base URL |
| `--namespace-id` | `14b39079-899b-4ca5-af43-a9339a69dfbf` | Target namespace ID |
| `--group` | `DEFAULT_GROUP` | Configuration group name (get_config.py only) |
| `--format` | `table` / `content` | Output format: table/json for list, content/json for get |
| `--search` | None | Search term to filter by dataId or group (list_configs.py only) |

## Common Workflows

**Find and read a configuration:**

```bash
# First, search for the config
scripts/list_configs.py --search application

# Then, read the specific config
scripts/get_config.py application-local.yml
```

**Export all configs as JSON:**

```bash
scripts/list_configs.py --format json > configs_list.json
scripts/get_config.py application-local.yml --format json > application_config.json
```

**Work with different environments:**

```bash
# Development namespace
scripts/list_configs.py --namespace-id dev-namespace-id

# Production namespace
scripts/list_configs.py --namespace-id prod-namespace-id
```

## API Endpoints

The scripts use these Nacos v3 Admin API endpoints:

- **List configs**: `GET /nacos/v3/admin/cs/history/configs?namespaceId={id}`
- **Get config**: `GET /nacos/v3/admin/cs/config?namespaceId={id}&groupName={group}&dataId={dataId}`

No authentication is required for these endpoints in the default configuration.
