directory="data";[! -d "$directory" ] && mkdir "$directory"
cd data
curl -O https://www.dol.gov/sites/dolgov/files/OFCCP/foia/files/FOIA-Log-7.1.23-12.31.23-508c.xlsx
curl -O https://www.dol.gov/sites/dolgov/files/OFCCP/foia/files/OFCCP-FOIA-Log-1-1-2015-7-6-2023.xlsx
in2csv OFCCP-FOIA-Log-1-1-2015-7-6-2023.xlsx > foia_log1.csv
in2csv FOIA-Log-7.1.23-12.31.23-508c.xlsx > foia_log2.csv
sed 's/ *, */,/g;s/ *$//' foia_log2.csv > foia_log2_fixed.csv
csvstack foia_log1.csv foia_log2_fixed.csv > combined_foia_log.csv
csvcut -x data/combined_foia_log.csv > data/combined_foia_log_fixed.csv
cd ..
python convert.py
