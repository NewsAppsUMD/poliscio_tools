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
            output_data.append([None, None, 75, "Department of Education", row['Request ID'], "Not Available", row['Requester Name'], row['Organization'], "Not Available", row['Requester Default Category'], row['Request Description'], "Not Available", row['Received Date'], row['Request Status'], "Not Available", row['Final Disposition'], row['Exemption Cited']])

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

    # Step 4: Clean up the CSV file
    fixed_filename = f"fixed_{csv_filename}"
    clean_csv(csv_filename, fixed_filename)

    # Step 5: Process the CSV file
    process_csv(fixed_filename)

if __name__ == "__main__":
    main()
