import requests
import csv
import sys
import os
import subprocess

def convert_to_csv(input_file, output_file):
    try:
        command = f"in2csv {input_file} > {output_file}"
        subprocess.run(command, shell=True, check=True)
        print(f"File converted to CSV: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert file to CSV: {e}")
        sys.exit(1)

def process_csv(filename):
    output_headers = ["wdt_ID", "ID", "agency", "agency_name", "official_agency_id", "request_type", "requester_name", "requester_org", "requester_category", "requester_category_name", "request_text", "request_target", "request_date", "request_status", "final_disposition", "closed_date", "exemptions"]
    output_data = []

    with open(filename, 'r') as original_file:
        reader = csv.DictReader(original_file)
        for row in reader:
            output_data.append([None, None, 174, "Occupational Safety and Health Administration (OSHA)", row['Request ID'], "Not Available", row['Requester Name'], row['Organization'], "Not Available", "Not Available", row['FOIA Log Description'], "Not Available", row['Original Received Date'], "Not Available", "Not Available", "Not Available", row['Exemption Cited']])

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

    # Step 2: Convert the downloaded file to CSV format
    csv_filename = f"{filename.split('.')[0]}.csv"
    convert_to_csv(filename, csv_filename)

    # Step 3: Process the CSV file
    process_csv(csv_filename)

if __name__ == "__main__":
    main()
