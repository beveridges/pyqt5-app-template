#!/bin/bash
# count_lines.sh — count total lines of Python code in all subdirectories

# Go to the directory where the script is located
cd "$(dirname "$0")"

# Count all .py lines recursively
echo "Counting lines of Python code..."
total=$(find . -name "*.py" -type f -exec cat {} + | wc -l)

echo "--------------------------------"
echo "Total lines of Python code: $total"
echo "--------------------------------"
