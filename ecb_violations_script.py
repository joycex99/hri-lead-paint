import csv
import collections


violations = {}
v_count = 0

# gather:

# SEVERITY, VIOLATION_TYPE, RESPONDANT_NAME

severities = collections.defaultdict(int)
violation_types = collections.defaultdict(int)
respondents = collections.defaultdict(int)

with open('DOB_ECB_Violations_active.csv') as f:
	reader = csv.DictReader(f)
	for row in reader:
		addr = row['RESPONDENT_HOUSE_NUMBER'] + ' ' + row['RESPONDENT_STREET'] + ', NY'
		if addr not in violations:
			violations[addr] = {
				'count': 0,
				'severities': collections.defaultdict(int),
				'violation_types': collections.defaultdict(int),
				# 'respondents': collections.defaultdict(int),
				# 'dob_numbers': []
			}
		violations[addr]['count'] +=1
		violations[addr]['severities'][row['SEVERITY']] += 1
		violations[addr]['violation_types'][row['VIOLATION_TYPE']] += 1
		# violations[addr]['respondents'][row['RESPONDENT_NAME']] += 1
		# violations[addr]['dob_numbers'].append(row['DOB_VIOLATION_NUMBER'])


sorted_list = sorted(violations.items(), key=lambda x: x[1]['count'], reverse=True)
sorted_violations = collections.OrderedDict(sorted_list)

# print(sorted_list[1])

with open('ecb_processed.csv', 'w+') as f:
	writer = csv.DictWriter(f, fieldnames=['address', 'num_violations', 'num_hazardous', 'types'])
	writer.writeheader()
	for k, v in sorted_violations.items():
		if k.strip() == ", NY": # skip row of empty addresses
			continue
		writer.writerow({'address': k, 
						 'num_violations': v['count'], 
						 'num_hazardous': v['severities']['Hazardous'],
						 'types': dict(v['violation_types'])})



# with open('DOB_ECB_Violations.csv') as f:
# 	reader = csv.DictReader(f)
# 	print(reader.fieldnames)

# 	with open('DOB_ECB_Violations_active.csv', 'w+') as out:
# 		writer = csv.DictWriter(out, fieldnames=reader.fieldnames)
# 		writer.writeheader()

# 		for row in reader:
# 			if row['ECB_VIOLATION_STATUS'] == 'ACTIVE':
# 				writer.writerow(row)
