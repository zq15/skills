#!/usr/bin/env python3
"""
List all configuration files in a Nacos namespace.
"""
import argparse
import json
import sys
import urllib.request
import urllib.error
from typing import Optional


def list_configs(
    base_url: str,
    namespace_id: str,
    search: Optional[str] = None
) -> dict:
    """
    List all configuration files in a Nacos namespace.

    Args:
        base_url: Nacos server base URL (e.g., http://localhost:8848)
        namespace_id: Namespace ID
        search: Optional search term to filter configs by dataId or group

    Returns:
        Dictionary containing the list of configurations
    """
    url = f"{base_url}/nacos/v3/admin/cs/history/configs?namespaceId={namespace_id}"

    try:
        with urllib.request.urlopen(url) as response:
            response_data = json.loads(response.read().decode())

            # Extract the actual config list from nested response
            if isinstance(response_data, dict) and 'data' in response_data:
                configs = response_data['data']
            else:
                configs = response_data

            # Handle case where configs is still a dict with nested data
            if isinstance(configs, dict) and 'data' in configs:
                configs = configs['data']

            # Ensure configs is a list
            if not isinstance(configs, list):
                configs = []

            # Filter if search term provided
            if search:
                configs = [
                    config for config in configs
                    if search.lower() in config.get('dataId', '').lower()
                    or search.lower() in config.get('groupName', '').lower()
                    or search.lower() in config.get('group', '').lower()
                ]

            return {
                'success': True,
                'data': configs,
                'count': len(configs)
            }
    except urllib.error.HTTPError as e:
        return {
            'success': False,
            'error': f'HTTP Error {e.code}: {e.reason}',
            'details': e.read().decode() if e.fp else ''
        }
    except urllib.error.URLError as e:
        return {
            'success': False,
            'error': f'Connection Error: {e.reason}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }


def main():
    parser = argparse.ArgumentParser(
        description='List all configuration files in a Nacos namespace'
    )
    parser.add_argument(
        '--base-url',
        default='http://localhost:8848',
        help='Nacos server base URL (default: http://localhost:8848)'
    )
    parser.add_argument(
        '--namespace-id',
        default='14b39079-899b-4ca5-af43-a9339a69dfbf',
        help='Namespace ID (default: 14b39079-899b-4ca5-af43-a9339a69dfbf)'
    )
    parser.add_argument(
        '--search',
        help='Search term to filter configs by dataId or group'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'table'],
        default='table',
        help='Output format (default: table)'
    )

    args = parser.parse_args()

    result = list_configs(args.base_url, args.namespace_id, args.search)

    if args.format == 'json':
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if result['success']:
            configs = result['data']
            if not configs:
                print("No configurations found.")
                return

            print(f"\nFound {result['count']} configuration(s):\n")
            print(f"{'DataID':<40} {'Group':<20} {'Type':<10}")
            print("-" * 70)
            for config in configs:
                data_id = config.get('dataId', 'N/A')[:39]
                group = config.get('groupName', config.get('group', 'N/A'))[:19]
                config_type = config.get('type', 'N/A')[:9]
                print(f"{data_id:<40} {group:<20} {config_type:<10}")
        else:
            print(f"Error: {result['error']}", file=sys.stderr)
            if result.get('details'):
                print(f"Details: {result['details']}", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
