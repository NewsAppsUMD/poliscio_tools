import requests
import csv
import sys
import os
import subprocess

def download_file(url, filename):
    response = requests.get(url, allow_redirects=True)
    with open(filename, 'wb') as file:
        file.write(response.content)
    print(f"File downloaded as {filename}")

def convert_to_csv(input_file, output_file):
    try:
        command = f"in2csv {input_file} > {output_file}"
        subprocess.run(command, shell=True, check=True)
        print(f"File converted to CSV: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert file to CSV: {e}")
        sys.exit(1)

def remove_first_two_rows(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        lines = infile.readlines()
        outfile.writelines(lines[2:])  # Skip the first two lines

def clean_csv(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            cleaned_line = line.replace(' *, *', ',').rstrip()
            outfile.write(cleaned_line + '\n')

def process_csv(filename):
    output_headers = ["wdt_ID", "ID", "agency", "agency_name", "official_agency_id", "request_type", "requester_name", "requester_org", "requester_category", "requester_category_name", "request_text", "request_target", "request_date", "request_status", "final_disposition", "closed_date", "exemptions"]
    output_data = []

    with open(filename, 'r') as original_file:
        reader = csv.DictReader(original_file)
        for row in reader:
            output_data.append([None, None, 294, "Office of the United States Trade Representative", row['FY Tracking Number'], "Not Available", row['Name of Requester'], row['Requester Organization Name '], "Not Available", "Not Available", row['Request Description'], "Not Available", row['Date Received'], "Not Available", "Not Available", row['Final Reply Date'], "Not Available"])

    processed_filename = f"../processed/{filename}"
    with open(processed_filename, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(output_headers)
        writer.writerows(output_data)
    
    print(f"Processed CSV saved as {processed_filename}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python convert.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    filename = url.split('/')[-1]

    # Step 1: Download the file
    download_file(url, filename)

    # Step 2: Convert the downloaded file to CSV format
    csv_filename = f"{filename.split('.')[0]}.csv"
    convert_to_csv(filename, csv_filename)

    # Step 3: Remove the first two rows
    trimmed_filename = f"trimmed_{csv_filename}"
    remove_first_two_rows(csv_filename, trimmed_filename)

    # Step 4: Clean up the CSV file
    fixed_filename = f"fixed_{trimmed_filename}"
    clean_csv(trimmed_filename, fixed_filename)

    # Step 5: Process the CSV file
    process_csv(fixed_filename)

if __name__ == "__main__":
    main()
