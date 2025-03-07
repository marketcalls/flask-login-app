#!/bin/bash

# This script runs during the build step on Vercel
echo "Running Vercel build script..."

# Ensure database directory exists
mkdir -p .data

# Initialize the database
python -c "from app import create_tables; create_tables()"

echo "Build script completed successfully!"
