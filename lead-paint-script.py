import csv
import collections


violations = {}
borough_counts = {}
v_count = 0
with open('Recent_Lead_Paint_Violations.csv') as f:
	reader = csv.DictReader(f)
	count = 0
	for row in reader:
		bid = row['BuildingID']
		if bid not in violations:
			violations[bid] = {
				'address': (row['HouseNumber'] + ' ' + row['StreetName'] + ', ' + 
							row['Borough'] + ' NY ' + row['Postcode']),
				'count': 1
			}
		else:
			violations[bid]['count'] += 1

		# personal curiosity
		borough = row['Borough']
		if borough not in borough_counts:
			borough_counts[borough] = 1
		else:
			borough_counts[borough] += 1
		v_count += 1

sorted_list = sorted(violations.items(), key=lambda x: x[1]['count'], reverse=True)
sorted_violations = collections.OrderedDict(sorted_list)

with open('lead_paint_processed.csv', 'w+') as f:
	writer = csv.DictWriter(f, fieldnames=['building_id', 'address', 'num_violations'])
	writer.writeheader()
	for k, v in sorted_violations.items():
		writer.writerow({'building_id': k, 
						 'address': v['address'], 
						 'num_violations': v['count']})

average_violations = v_count / len(violations)
print(borough_counts)
print(average_violations)


