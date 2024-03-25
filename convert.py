import csv

original_file = open("data/combined_foia_log_fixed.csv", "r")
reader = csv.DictReader(original_file)

output_headers = ["wdt_ID","ID","agency","agency_name","official_agency_id","request_type","requester_name","requester_org","requester_category","requester_category_name","request_text","request_target","request_date","request_status","final_disposition","closed_date","exemptions"]
output_data = []

for row in reader:
    output_data.append([None, None, 169, "Office of Federal Contract Compliance Programs", row['Request ID'], "Not Available", "Not Available", "Not Available", "Not Available", "Not Available", row['Summary of Request'], "Not Available", row['Received Date'], "Not Available", row['Final Disposition'], row['Closed Date'], "Not Available"])

output_file = open("processed/OFCCP FOIA Logs.csv", "w")
writer = csv.writer(output_file)
writer.writerow(output_headers)
writer.writerows(output_data)
