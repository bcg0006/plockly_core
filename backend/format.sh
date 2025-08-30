#!/bin/bash

# Code formatting script for Plockly backend
# Run this script before committing to ensure code meets CI/CD standards

echo "🔧 Formatting Python code with Black and isort..."

# Check if Black is installed
if ! command -v black &> /dev/null; then
    echo "❌ Black is not installed. Installing..."
    pip install black
fi

# Check if isort is installed
if ! command -v isort &> /dev/null; then
    echo "❌ isort is not installed. Installing..."
    pip install isort
fi

# Run Black formatter
echo "📝 Running Black formatter..."
black . --check
if [ $? -eq 0 ]; then
    echo "✅ Black formatting check passed"
else
    echo "⚠️  Some files need formatting. Running Black..."
    black .
    echo "✅ Black formatting completed"
fi

# Run isort to sort imports
echo "📚 Running isort to sort imports..."
isort . --check-only
if [ $? -eq 0 ]; then
    echo "✅ Import sorting check passed"
else
    echo "⚠️  Some imports need sorting. Running isort..."
    isort .
    echo "✅ Import sorting completed"
fi

# Run flake8 for linting
echo "🔍 Running flake8 for linting..."
if ! command -v flake8 &> /dev/null; then
    echo "❌ flake8 is not installed. Installing..."
    pip install flake8
fi

flake8 . --max-line-length=88 --extend-ignore=E203,W503
if [ $? -eq 0 ]; then
    echo "✅ Linting check passed"
else
    echo "⚠️  Some linting issues found. Please fix them."
    exit 1
fi

echo "🎉 All formatting and linting checks passed!"
echo "💡 You can now commit your code with confidence!"
