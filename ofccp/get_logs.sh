#!/bin/bash

# Prompt the user for the URL
read -p "Enter the URL: " url

# Extract the file name from the URL
filename=$(basename "$url")

# Download the file from the provided URL
curl -O "$url"

# Convert the downloaded file to CSV format
in2csv "$filename" > "${filename%.*}.csv"

# Clean up the CSV file
sed 's/ *, */,/g;s/ *$//' "${filename%.*}.csv" > "${filename%.*}_fixed.csv"

# Uncomment the following line if you want to use csvcut
# csvcut -x "${filename%.*}_fixed.csv" > "${filename%.*}_fixed.csv"

# Run the Python script to process the data
python convert.py "${filename%.*}_fixed.csv"