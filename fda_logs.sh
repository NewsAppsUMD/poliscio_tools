mkdir -p processed
cd data
in2csv fda_foia_log_-_march_2024.xlsx > fda_foia_log_march_2024.csv
csvcut -x fda_foia_log_march_2024.csv > fda_foia_log_march_2024_cleaned.csv
cd ..
python convert_fda.py