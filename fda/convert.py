import requests
import subprocess
import csv
import os

def get_filename_from_url(url):
    response = requests.get(url, allow_redirects=True)
    filename = None
    if 'content-disposition' in response.headers:
        content_disposition = response.headers['content-disposition']
        if 'filename=' in content_disposition:
            filename = content_disposition.split('filename=')[1]
            if filename.startswith('"') and filename.endswith('"'):
                filename = filename[1:-1]
    return filename

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

def process_csv(filename):
    output_headers = ["wdt_ID", "ID", "agency", "agency_name", "official_agency_id", "request_type", "requester_name", "requester_org", "requester_category", "requester_category_name", "request_text", "request_target", "request_date", "request_status", "final_disposition", "closed_date", "exemptions"]
    output_data = []

    with open(filename, 'r') as original_file:
        reader = csv.DictReader(original_file)
        for row in reader:
            output_data.append([None, None, 102, "Food and Drug Administration", row['Control #'], "Not Available", "Not Available", "Not Available", "Not Available", "Not Available", row['Subject'], "Not Available", row['Recd Date'], "Not Available", "Not Available", "Not Available", "Not Available"])

    processed_filename = f"../processed/{filename.split('.')[0]}.csv"
    with open(processed_filename, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(output_headers)
        writer.writerows(output_data)
    
    print(f"Processed CSV saved as {processed_filename}")

def main():
    url = input("Enter the URL: ")
    filename = get_filename_from_url(url)
    
    if filename:
        print(f"Filename retrieved: {filename}")
        download_file(url, filename)
    else:
        print("Failed to retrieve the filename. Downloading with default name 'downloaded_file'.")
        filename = 'downloaded_file'
        download_file(url, filename)

    csv_filename = f"{filename.split('.')[0]}.csv"
    convert_to_csv(filename, csv_filename)
    process_csv(csv_filename)

if __name__ == "__main__":
    main()
