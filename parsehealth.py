#!/usr/bin/python
# Simple Python script to parse Apple Health Values out of the export.xml into a pipe delimited txt file
# Modify the script to generate a CSV file as output format

import re, sys, os, datetime
from datetime import datetime
import csv

# Assumes you run the script in same location as the exported data. 
# In German version of Apple Health the file is called 'Exportieren.xml'
healthlog = open("Exportieren.xml","r")

# Open Parsed results csv file
healthresults = open("AppleHealthData.csv","w")
writer = csv.writer(healthresults, delimiter=',')
writer.writerow(["DateTime", "Source", "HealthType", "HealthValue"])

# Initi counter
count =0

#Init Health type value dictionary

valdic ={}
sourcedic ={}

#determine number of lines in export.xml
num_lines = sum(1 for line in open("Exportieren.xml"))

FMT = '%Y-%m-%d %H:%M:%S'

# loop through export.eml
for line in healthlog:
	#find record types
	if re.search(r"<Record type=", line):
		recordtype = re.search(r"<Record type=\"\S+\"",line)
		recordtypeval = recordtype.group()

		# Add record types to value dictionary
		valdic[recordtypeval[15:-1]] = count

		# get source of value			
		sourceName =re.search(r"sourceName\S\S\S+\s+\S+",line)
                sourceNameval = sourceName.group()
		sourcedic [sourceNameval[12:]] = count

		# Get value of record type 
		healthdata = re.search(r"value\S\S\w+",line)
                if healthdata is None:
			healthdata = "No Val"
		else: 
			if recordtypeval[15:-1] == "KCategoryTypeIdentifierSleepAnalysis":
				starttime = re.search(r"startDate\S\S\d+\-\d+\-\d+\s+\d+\:\d+\:\d+",line)
				endtime = re.search(r"endDate\S\S\d+\-\d+\-\d+\s+\d+\:\d+\:\d+",line)
				tdelta = datetime.strptime(endtime.group()[9:], FMT) - datetime.strptime(starttime.group()[11:], FMT)  
				healthdataval = "0000000" + str(tdelta)[:1]
			else:
				healthdataval = healthdata.group()

		#Get end date/time of data collection 
		datetime2 = re.search(r"endDate\S\S\d+\-\d+\-\d+\s+\d+\:\d+\:\d+",line)
		datetime2val = datetime2.group()

		# Output results to file
		row = []
                row.append(str(datetime2val[9:]))
                row.append(str(sourceNameval[12:]))
                row.append(str(recordtypeval[15:-1]))
                row.append(str(healthdataval[7:]))
                writer.writerow(row)
		count = count +1


		# print progress hash
		if count % 10000 == 0:
			print '{counts} of {nums}'.format(counts=count, nums=num_lines)
			sys.stdout.flush()

#Close files
healthlog.close()
healthresults.close()

#Print values parsed
print "Health Values Captured"
for key in valdic:
	print key
print "Device Sources of Health Data"
for key in sourcedic:
	print key


