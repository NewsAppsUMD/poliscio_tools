import csv
import sys

# Check if the CSV file name is provided as an argument
if len(sys.argv) < 2:
    print("Usage: python convert.py <csv_file_name>")
    sys.exit(1)

csv_file = sys.argv[1]

original_file = open(csv_file, "r")
reader = csv.DictReader(original_file)

output_headers = ["wdt_ID", "ID", "agency", "agency_name", "official_agency_id", "request_type", "requester_name", "requester_org", "requester_category", "requester_category_name", "request_text", "request_target", "request_date", "request_status", "final_disposition", "closed_date", "exemptions"]
output_data = []

for row in reader:
    output_data.append([None, None, 169, "Office of Federal Contract Compliance Programs", row['Request ID'], "Not Available", "Not Available", "Not Available", "Not Available", "Not Available", row['Request Description'], "Not Available", row['Received Date'], "Not Available", row['Final Disposition'], row['Closed Date'], "Not Available"])

output_file = open(f"../processed/{csv_file}.csv", "w", newline='')
writer = csv.writer(output_file)
writer.writerow(output_headers)
writer.writerows(output_data)

original_file.close()
output_file.close()