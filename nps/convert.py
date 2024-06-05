import requests
import csv

def download_file(url, filename):
    response = requests.get(url, allow_redirects=True)
    with open(filename, 'wb') as file:
        file.write(response.content)
    print(f"File downloaded as {filename}")

def process_csv(filename):
    output_headers = ["wdt_ID", "ID", "agency", "agency_name", "official_agency_id", "request_type", "requester_name", "requester_org", "requester_category", "requester_category_name", "request_text", "request_target", "request_date", "request_status", "final_disposition", "closed_date", "exemptions"]
    output_data = []

    with open(filename, 'r') as original_file:
        reader = csv.DictReader(original_file)
        for row in reader:
            output_data.append([None, None, 10, "National Park Service", row['Tracking Number'], row['Request Type'], row['Requester'], row['Requester Organization'], "Not Available", "Not Available", row['Description'], "Not Available", row['Received Date'], row['Phase'], row['Final Disposition'], row['Closed Date'], "Not Available"])

    processed_filename = f"../processed/{filename.split('.')[0]}_processed.csv"
    with open(processed_filename, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(output_headers)
        writer.writerows(output_data)
    
    print(f"Processed CSV saved as {processed_filename}")

def main():
    url = input("Enter the URL of the CSV file: ")
    filename = url.split('/')[-1]  # Extract the filename from the URL
    
    download_file(url, filename)
    process_csv(filename)

if __name__ == "__main__":
    main()
