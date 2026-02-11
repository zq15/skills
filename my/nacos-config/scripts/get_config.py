#!/usr/bin/env python3
"""
Get a specific configuration file from Nacos.
"""
import argparse
import json
import sys
import urllib.request
import urllib.error
import urllib.parse
from typing import Optional


def get_config(
    base_url: str,
    namespace_id: str,
    data_id: str,
    group_name: str = "DEFAULT_GROUP"
) -> dict:
    """
    Get a specific configuration file from Nacos.

    Args:
        base_url: Nacos server base URL (e.g., http://localhost:8848)
        namespace_id: Namespace ID
        data_id: Configuration data ID (e.g., application-local.yml)
        group_name: Group name (default: DEFAULT_GROUP)

    Returns:
        Dictionary containing the configuration content
    """
    params = urllib.parse.urlencode({
        'namespaceId': namespace_id,
        'groupName': group_name,
        'dataId': data_id
    })
    url = f"{base_url}/nacos/v3/admin/cs/config?{params}"

    try:
        with urllib.request.urlopen(url) as response:
            response_text = response.read().decode('utf-8')

            # Try to parse as JSON first (v3 API returns JSON)
            try:
                response_data = json.loads(response_text)

                # Extract content from nested structure
                if isinstance(response_data, dict):
                    # Handle v3 API response format
                    if 'data' in response_data and isinstance(response_data['data'], dict):
                        content = response_data['data'].get('content', response_text)
                    else:
                        content = response_data.get('content', response_text)
                else:
                    content = response_text
            except json.JSONDecodeError:
                # If not JSON, treat as raw content
                content = response_text

            return {
                'success': True,
                'dataId': data_id,
                'group': group_name,
                'namespaceId': namespace_id,
                'content': content
            }
    except urllib.error.HTTPError as e:
        error_detail = e.read().decode() if e.fp else ''
        return {
            'success': False,
            'error': f'HTTP Error {e.code}: {e.reason}',
            'details': error_detail,
            'dataId': data_id,
            'group': group_name
        }
    except urllib.error.URLError as e:
        return {
            'success': False,
            'error': f'Connection Error: {e.reason}',
            'dataId': data_id,
            'group': group_name
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}',
            'dataId': data_id,
            'group': group_name
        }


def main():
    parser = argparse.ArgumentParser(
        description='Get a specific configuration file from Nacos'
    )
    parser.add_argument(
        'data_id',
        help='Configuration data ID (e.g., application-local.yml)'
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
        '--group',
        default='DEFAULT_GROUP',
        help='Group name (default: DEFAULT_GROUP)'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'content'],
        default='content',
        help='Output format: content (raw config) or json (metadata+content) (default: content)'
    )

    args = parser.parse_args()

    result = get_config(
        args.base_url,
        args.namespace_id,
        args.data_id,
        args.group
    )

    if args.format == 'json':
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if result['success']:
            print(result['content'])
        else:
            print(f"Error retrieving config '{args.data_id}' from group '{args.group}':", file=sys.stderr)
            print(f"  {result['error']}", file=sys.stderr)
            if result.get('details'):
                print(f"  Details: {result['details']}", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
