#!/usr/bin/env python3
"""
Log Analyzer - Analyzes JSON-formatted API request logs and generates statistics.
Usage: python log_analyzer.py <logfile>
"""

# Library imports - using only Python's standard libraries
import json
import sys
from collections import Counter


"""
Function to analyze log file and return request statistics.
"""
def analyze_logs(file_path: str) -> tuple:
    """Process log file and return request statistics."""
    # Initialize counters
    total = 0
    errors = 0
    error_counts = Counter()

    try:
        # Using 'with' for automatic file closing
        with open(file_path) as f:
            for line in f:
                try:
                    # Parse JSON
                    entry = json.loads(line)
                    # Skip incomplete entries
                    if not all(k in entry for k in ['endpoint', 'status_code']):
                        continue
                    
                    total += 1  # Count valid requests
                    # HTTP status codes >= 400 indicate errors
                    if entry['status_code'] >= 400:
                        errors += 1
                        # Counter automatically initializes counts
                        error_counts[entry['endpoint']] += 1
                except json.JSONDecodeError:
                    # Skip invalid JSON
                    continue

        # Return total requests, error requests, and top 3 endpoints with most errors
        return total, errors, error_counts.most_common(3)
    except FileNotFoundError:
        # Print error and exit
        print(f"Error: File not found: {file_path}")
        sys.exit(1)


"""
Main entry point. Uses analyze_logs to process log file and print statistics.
"""
def log_analyzer():
    # Validate command line arguments - expect one argument after the script name: the log file
    if len(sys.argv) != 2:
        print("Usage: python log_analyzer.py <logfile>")
        sys.exit(1)

    # Get file path from command line argument
    file_path = sys.argv[1]
    # Process logs and get statistics
    total, errors, top_errors = analyze_logs(file_path)

    # Print results
    print("\nLog analysis results")
    print("-" * 50)  # Separator line
    print(f"Total requests: {total}")
    print(f"Error requests: {errors}")
    print("\nTop 3 endpoints with most errors:")
    # Unpack and format error statistics
    for endpoint, count in top_errors:
        print(f"  {endpoint}: {count} errors")


if __name__ == "__main__":
    log_analyzer()
