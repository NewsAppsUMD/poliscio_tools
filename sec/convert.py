import csv
import requests
import argparse
import os

def download_file(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
    }
    local_filename = url.split('/')[-1]
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'w', encoding='latin1') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk.decode('latin1'))
    return local_filename

def preprocess_csv(input_filename):
    request_type = None
    output_data = []
    
    with open(input_filename, 'r', encoding='latin1') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        headers.append("Request Type")
        
        for row in reader:
            if row[0].startswith("Total No of Requests"):
                continue
            if row[0].startswith("Request Type:"):
                request_type = row[0].split(":")[1].strip()
                continue
            if request_type:
                row.append(request_type)
            output_data.append(row)
    
    output_filename = os.path.splitext(input_filename)[0] + "_processed.csv"
    with open(output_filename, 'w', newline='', encoding='latin1') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(output_data)
    
    return output_filename

def process_csv(filename):
    output_headers = ["wdt_ID", "ID", "agency", "agency_name", "official_agency_id", "request_type", "requester_name", "requester_org", "requester_category", "requester_category_name", "request_text", "request_target", "request_date", "request_status", "final_disposition", "closed_date", "exemptions"]
    output_data = []

    with open(filename, 'r', encoding='latin1') as original_file:
        reader = csv.DictReader(original_file)
        for row in reader:
            if 'Requester Default Category' in row:
                output_data.append([None, None, 300, "Securities and Exchange Commission", row['Request ID'], "Not Available", row['Requester Name'], row['Organization'], "Not Available", row['Requester Default Category'], row['Request Description'], "Not Available", row['Received Date'], row['Request Status'], "Not Available", row['Final Disposition'], row['Exemption Cited']])
            else:
                output_data.append([None, None, 300, "Securities and Exchange Commission", row['Request ID'], "Not Available", row['Requester Name'], row['Organization'], "Not Available", "Not Available", row['Request Description'], "Not Available", row['Received Date'], row['Request Status'], "Not Available", row['Final Disposition'], "Not Available"])

    processed_filename = f"../processed/{filename}"
    with open(processed_filename, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(output_headers)
        writer.writerows(output_data)
    
    print(f"Processed CSV saved as {processed_filename}")

def main():
    parser = argparse.ArgumentParser(description="Download and process a CSV file.")
    parser.add_argument("url", help="The URL of the CSV file to download.")
    args = parser.parse_args()
    
    local_filename = download_file(args.url)
    output_filename = preprocess_csv(local_filename)
    process_csv(output_filename)

if __name__ == "__main__":
    main()
