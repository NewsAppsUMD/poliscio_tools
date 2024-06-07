#!/bin/bash

# Check if the sqlite-utils command is installed
if ! command -v sqlite-utils &> /dev/null
then
    echo "sqlite-utils could not be found. Please install it using 'pip install sqlite-utils'."
    exit 1
fi

# Define the database name and table name
DB_NAME="foia_logs.db"
TABLE_NAME="requests"

# Delete the database if it exists
if [ -f "$DB_NAME" ]; then
    echo "Deleting existing database $DB_NAME..."
    rm "$DB_NAME"
fi

# Directory containing the processed CSV files
DIRECTORY="processed"

# Iterate through each CSV file in the directory
for csv_file in "$DIRECTORY"/*.csv
do
    if [ -f "$csv_file" ]; then
        echo "Processing $csv_file..."
        sqlite-utils insert "$DB_NAME" "$TABLE_NAME" "$csv_file" --csv --detect-types
        echo "Inserted $csv_file into $TABLE_NAME table."
    else
        echo "No CSV files found in $DIRECTORY."
        exit 1
    fi
done

# Add full-text search on the specified columns
echo "Adding full-text search to $TABLE_NAME table..."
sqlite-utils enable-fts "$DB_NAME" "$TABLE_NAME" requester_name requester_org request_text

echo "All CSV files have been processed, inserted into the database, and full-text search has been enabled."
