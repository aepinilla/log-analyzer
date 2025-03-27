# Log Analyzer

A Python command-line tool that processes JSON-formatted log files and generates key statistics about API requests.

## Features

- Processes JSON-formatted log files line by line
- Calculates total number of API requests
- Identifies and counts error requests (status code >= 400)
- Lists top 3 endpoints with the most errors
- Handles invalid JSON and missing fields gracefully

## Requirements

- Python 3.x
- No additional dependencies required (uses only Python standard libraries)

## Installation

Clone this repository or download the source code:

```bash
git clone github.com/aepinilla/log-analyzer
cd log-analyzer
```

## Usage

Run the script by providing a path to your log file:

```bash
python log_analyzer.py sample.log
# or
python3 log_analyzer.py sample.log
```

### Expected Log Format

Each line in the log file should be a JSON object with the following fields:

```json
{
    "timestamp": "2025-03-14T12:34:56Z",
    "endpoint": "/api/data",
    "status_code": 200
}
```

### Sample Output

```
Log Analysis Results
--------------------
Total Requests: 105
Error Requests: 74

Top 3 Endpoints with Most Errors:
  /api/users: 18 errors
  /api/auth: 16 errors
  /api/data: 14 errors
```

## Error Handling

The script handles several types of errors:

- Invalid JSON entries
- Missing required fields
- File not found
- IO errors

Warnings are printed to the console when issues are encountered, but processing continues for valid entries.

## Project Structure

```
log-analyzer/
├── log_analyzer.py  # Main script
├── README.md       # Documentation
└── sample.log      # Sample log file for testing
```

## Development Notes

- Written in pure Python without external dependencies for maximum portability
- Uses type hints for better code maintainability
- Includes comprehensive error handling and validation