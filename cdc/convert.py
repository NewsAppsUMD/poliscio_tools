import requests
import subprocess
import csv
import os
import zipfile
from datetime import datetime

def download_file(url, filename):
    response = requests.get(url, allow_redirects=True)
    with open(filename, 'wb') as file:
        file.write(response.content)
    print(f"File downloaded as {filename}")

def unzip_file(zip_filename, extract_dir):
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        for member in zip_ref.namelist():
            # Remove the top-level folder from the path
            member_path = member.split('/', 1)[-1]
            target_path = os.path.join(extract_dir, member_path)
            # Create directories if they do not exist
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            # Extract file
            with zip_ref.open(member) as source, open(target_path, 'wb') as target:
                target.write(source.read())
    print(f"File unzipped to {extract_dir}")

def rename_files_in_directory(directory):
    for filename in os.listdir(directory):
        new_filename = filename.replace(' ', '_')
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))

def get_all_xlsx_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.xlsx')]

def convert_to_csv(input_file, output_file, remove_first_line=True):
    try:
        temp_output_file = "temp_" + output_file
        command = f"in2csv {input_file} > {temp_output_file}"
        subprocess.run(command, shell=True, check=True)
        
        if remove_first_line:
            # Remove the first line
            with open(temp_output_file, 'r') as temp_file, open(output_file, 'w') as final_file:
                next(temp_file)  # Skip the first line
                for line in temp_file:
                    final_file.write(line)
            os.remove(temp_output_file)
            print(f"File converted to CSV and first line removed: {output_file}")
        else:
            os.rename(temp_output_file, output_file)
            print(f"File converted to CSV: {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"Failed to convert file to CSV: {e}")

def process_csv(filename):
    output_headers = ["wdt_ID", "ID", "agency", "agency_name", "official_agency_id", "request_type", "requester_name", "requester_org", "requester_category", "requester_category_name", "request_text", "request_target", "request_date", "request_status", "final_disposition", "closed_date", "exemptions"]
    output_data = []

    with open(filename, 'r') as original_file:
        reader = csv.DictReader(original_file)
        for row in reader:
            if 'Received Date' in row:
                date = row["Received Date"]
            else:
                date = None
            output_data.append([None, None, 100, "Centers for Disease Control and Prevention (CDC)", row['Request ID'], "Not Available", row["Requester Name"], row["Organization"], "Not Available", "Not Available", row['Request Description'], "Not Available", date, "Not Available", "Not Available", "Not Available", "Not Available"])

    processed_filename = f"../processed/{filename.split('.')[0]}.csv"
    with open(processed_filename, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(output_headers)
        writer.writerows(output_data)
    
    print(f"Processed CSV saved as {processed_filename}")

def main():
    url = "https://foia.cdc.gov/docs/logfiles/CDC%20FOIA%20Log%20Files.zip"
    zip_filename = "CDC_FOIA_Log_Files.zip"
    extract_dir = "extracted/"

    print("Downloading the zip file...")
    download_file(url, zip_filename)

    print("Unzipping the file...")
    unzip_file(zip_filename, extract_dir)

    # Rename the extracted files to replace spaces with underscores
    print("Renaming extracted files to replace spaces with underscores...")
    rename_files_in_directory(extract_dir)

    print("Finding all xlsx files...")
    xlsx_files = get_all_xlsx_files(extract_dir)
    if xlsx_files:
        for xlsx_file in xlsx_files:
            xlsx_path = os.path.join(extract_dir, xlsx_file)
            csv_filename = f"{os.path.basename(xlsx_path).split('.')[0]}.csv"
            remove_first_line = csv_filename not in ["FY18_Q4.csv", "FY19_Q3.csv", "FY18_Q3.csv", "FY19_Q1.csv", "FY19_Q2.csv"]
            print(f"Converting {xlsx_path} to CSV and removing the first line (if required)...")
            convert_to_csv(xlsx_path, csv_filename, remove_first_line)
            print("Processing the CSV file...")
            process_csv(csv_filename)
    else:
        print("No xlsx files found in the extracted directory.")

if __name__ == "__main__":
    main()
