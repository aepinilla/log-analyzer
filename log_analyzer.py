#!/usr/bin/env python3
"""
Log Analyzer - A command-line tool for processing JSON-formatted log files.

This script analyzes log files containing JSON-formatted API request logs and generates
key statistics including total requests, error counts, and problematic endpoints.
"""

from typing import Dict, List, Tuple, Optional
import json
import sys
from collections import Counter
from pathlib import Path


def validate_log_entry(entry: Dict) -> bool:
    """Validate that a log entry contains all required fields with correct types.

    Args:
        entry (Dict): The log entry to validate

    Returns:
        bool: True if entry is valid, False otherwise
    """
    try:
        if not all(k in entry for k in ['timestamp', 'endpoint', 'status_code']):
            print(f"Warning: Missing required fields in log entry: {entry}")
            return False
        
        if not isinstance(entry['endpoint'], str):
            print(f"Warning: Invalid endpoint type in entry: {entry}")
            return False
            
        if not isinstance(entry['status_code'], int):
            print(f"Warning: Invalid status code type in entry: {entry}")
            return False
            
        return True
    except Exception as e:
        print(f"Warning: Error validating entry: {e}")
        return False


def analyze_logs(file_path: str) -> Tuple[int, int, List[Tuple[str, int]]]:
    """Process the log file and compute request statistics.
    
    Args:
        file_path (str): Path to the log file containing JSON-formatted log entries
        
    Returns:
        Tuple[int, int, List[Tuple[str, int]]]: A tuple containing:
            - Total number of valid requests processed
            - Number of requests that resulted in errors (status code >= 400)
            - List of tuples (endpoint, error_count) for the top 3 endpoints with most errors
            
    Raises:
        FileNotFoundError: If the specified log file doesn't exist
        IOError: If there are issues reading the log file
    """
    total = errors = 0
    error_counts = Counter()

    try:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        if not path.is_file():
            raise IOError(f"Path is not a file: {file_path}")

        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    entry = json.loads(line.strip())
                    if not validate_log_entry(entry):
                        print(f"Warning: Invalid entry at line {line_num}")
                        continue
                    
                    total += 1
                    if entry['status_code'] >= 400:
                        errors += 1
                        error_counts[entry['endpoint']] += 1
                except json.JSONDecodeError as e:
                    print(f"Warning: Invalid JSON at line {line_num}: {e}")
                    continue
                except Exception as e:
                    print(f"Warning: Unexpected error at line {line_num}: {e}")
                    continue

        return total, errors, error_counts.most_common(3)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"Error: Failed to read file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Unexpected error: {e}")
        sys.exit(1)


def log_analyzer() -> None:
    """Main entry point of the script.
    
    Validates command-line arguments, processes the log file, and displays results.
    
    Exit codes:
        0: Successful execution
        1: Invalid command-line arguments or file error
    """
    if len(sys.argv) != 2:
        print("Usage: python log_analyzer.py <logfile>")
        sys.exit(1)

    file_path = sys.argv[1]
    total, errors, top_errors = analyze_logs(file_path)

    print("\nLog Analysis Results")
    print("-" * 20)
    print(f"Total Requests: {total}")
    print(f"Error Requests: {errors}")
    print("\nTop 3 Endpoints with Most Errors:")
    for endpoint, count in top_errors:
        print(f"  {endpoint}: {count} errors")


if __name__ == "__main__":
    log_analyzer()
